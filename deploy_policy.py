from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.resource import PolicyClient, ResourceManagementClient
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.policyinsights import PolicyInsightsClient
from azure.mgmt.policyinsights.models import Remediation, RemediationFilters
from azure.mgmt.resource.policy.models import PolicyDefinition, PolicySetDefinition, PolicyDefinitionReference, Identity, PolicyAssignment
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters
from policies import *
import time
import uuid

#Create the variables
token = DefaultAzureCredential()
management_group_id = ""
subscription_id = ""
group_name = "AZ500Test"

#Create the objects 
policy_client = PolicyClient(credential=token, subscription_id=subscription_id)
policy_insights_client = PolicyInsightsClient(credential=token, subscription_id=subscription_id)
#resource_management_client = ResourceManagementClient(credential=token, subscription_id=subscription_id)
#subscription_client = SubscriptionClient(credential=token)
authorization_client = AuthorizationManagementClient(token, subscription_id)

#Set the scopes
scopeRG = '/subscriptions/{}/resourceGroups/{}'.format(subscription_id, group_name)
scopeSubscription = '/subscriptions/{}'.format(subscription_id)
scopeMG = '/providers/Microsoft.Management/managementGroups/{}'.format(management_group_id)

    
def create_policy_def(policy_dict):
    """Take the dictionary of json policies and create them in Azure. Then return the ids of them in a list."""
    ref_id = []
    policy_def_id = []
    
    
    for k, v in policy_dict.items():

        try:
            result = policy_client.policy_definitions.create_or_update_at_management_group(policy_definition_name=f"{k}_TEST",
                                                                management_group_id=management_group_id,
                                                                parameters=v
                                                                )   
            print(f"Successfully created/updated policy definition for {k}")
        except Exception as e:
            print(f"An error has occured: {e}")
       
       #Append items to list so we can return an use for next function.
        policy_definition_reference_id = result.id
        policy_def_id.append(policy_definition_reference_id)

        #Make references that PolicySetDefinition is going to use.
        reference = PolicyDefinitionReference(policy_definition_id=policy_definition_reference_id)
        ref_id.append(reference)
        
    
    
    return ref_id, policy_def_id

    #except (FileNotFoundError, json.JSONDecodeError) as ex:
        #print(f"Error loading JSON file: {ex}")

def delete_policy_def(policy_dict):
    for k in policy_dict:
        policy_client.policy_definitions.delete_at_management_group(policy_definition_name=f"{k}_TEST", management_group_id=management_group_id)

        print(f"Successfully deleted policy definition for {k}")

        
def create_initiative():
    """Create the policy initiative with the definitions we created"""
    #Make sure if you change the name you go to remediation function and change name of the .get(""). You need the name for the definition reference ids.
    policy_initiative_name = "TEST_DIAG_Setting"
    policy_initiative_display_name = "TEST_DIAG_Setting"
    policy_initiative_description = "This policy initiative contains multiple policy definitions to enable logging on resources."
    references, def_id = create_policy_def(policy_list)

    #Create instance of set definitons class so we can feed it to the create method.
    policy_initiative = PolicySetDefinition(
        policy_definitions=references,
        display_name=policy_initiative_display_name,
        description=policy_initiative_description,
        metadata={"category": "Compliance"}
    )

    #Create the initiative with initiative instance from above.
    try:
        result = policy_client.policy_set_definitions.create_or_update(
            policy_set_definition_name=policy_initiative_name,
            parameters=policy_initiative
            )
        print(f"Policy initiative '{policy_initiative_name}' created or updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return result.id, def_id


def assign_initiative():
    """Assign the initiative we just created and assign roles for the identity so we can remediate with it."""
    #Get identity so we can remediate with it.
    identity = Identity(type="SystemAssigned")
    identity.tenant_id = ""

    #Get Initiative ID
    init_id, def_id = create_initiative()

    #Create the assignment instance.
    policy_assignment = PolicyAssignment(identity=identity, location="eastus", display_name="Deploy Diag Settings to Resources", 
                                         policy_definition_id=init_id, description="Resource does not have diagnostic setting.",
                                         metadata={"category": "Monitoring"})
    
    #Assign the initiatve using the assignment instance.
    try:
        result = policy_client.policy_assignments.create(scope=scopeSubscription, policy_assignment_name=policy_assignment.display_name, parameters=policy_assignment)
        print(f"Status: Initiative Assigned")
    except Exception as e:
        print(f"An error occurred: {e}")

    #Assign a role for managed identity.
    #First sleep and wait 10 seconds after creation of policy assignment to give the managed identity time to be created.
    time.sleep(10) 

     # Get the managed identity's principal ID
    managed_identity_principal_id = result.identity.principal_id
    #print(managed_identity_principal_id) #Use this to make sure it works.

    #Roles to assign identity. Find the role id you need an put into this list.
    roles = ["749f88d5-cbae-40b8-bcfc-e573ddc772fa", "92aaf0da-9dab-42b6-94a3-d43ce8d16293"] #Monitoring Contributor and Log Analytic Contributor
    
    # Assign the role to the managed identity
    for role in roles:

        try:
            role_assignment_params = RoleAssignmentCreateParameters(
                role_definition_id=f"/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/{role}",
                principal_id=managed_identity_principal_id,
                principal_type="ServicePrincipal"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            role_assignment_result = authorization_client.role_assignments.create(
                scope=f"/subscriptions/{subscription_id}",
                role_assignment_name=str(uuid.uuid4()),
                parameters=role_assignment_params
            )

            print(f"Role assigned to managed identity: {role_assignment_result.id}")
    
    return result.id, def_id

def check_and_cancel_existing_remediations(policy_assignment_id=None, policy_definition_reference_id=None, resource_group_name=None):
    """Check for existing remediations and cancel them if found."""
    existing_remediations = policy_insights_client.remediations.list_for_resource_group(resource_group_name=resource_group_name)
    print(existing_remediations)

    for remediation in existing_remediations:
        #print(remediation.id)
        #if remediation.policy_assignment_id == policy_assignment_id and remediation.policy_definition_reference_id == policy_definition_reference_id:
            # Cancel the existing remediation
        policy_insights_client.remediations.delete_at_resource_group(resource_group_name=resource_group_name, remediation_name=remediation.name)
        print(f"Canceled existing remediation: {remediation.name}")



def remediation():
    """Remediate the non compliant resources"""
    
    #Assignment ID and Definition Names
    assignment_id, def_names = assign_initiative()
    
    #Use this to get names for the remediation task
    names = [name.split("/")[-1] for name in def_names]
    
    #We need to retrieve the policy definition reference id inside the initiative so we can reference it in the remediation task. 
    #This will grab the initiative with the name "TEST_DIAG_SETTING". Change the name to whataver your initiative is.
    try:
        initiative = policy_client.policy_set_definitions.get("TEST_DIAG_Setting")
    
        #Create the reference id list.
        definitions = initiative.policy_definitions
    except Exception as e:
        print(f"An error occured: {e}")
    #for definition in definitions:
        #ref_id = definition.policy_definition_reference_id

    #List comprehension for the reference ids. Use the above if you don't want to use comprehension.
    ref_ids = [definition.policy_definition_reference_id for definition in definitions]
    #print(ref_ids) # Check to confirm they are in list.
    
    #remdiate_location = RemediationFilters(locations=["All"])  #Needed if you want to secifiy location on the remediation. Didn't work for me so I left it out.
    #location = remdiate_location.locations

    #Cancel any ongoing remediations before creating yours.
    #I was just assuing this for testing. If you have actual remediations going on you will need to find 
    # a different way than using this because this will cancel any actual remediations you have going on.
    check_and_cancel_existing_remediations(resource_group_name="az500test") 
    
    # Iterate through ids and names simultaneously using zip
    for id, name in zip(ref_ids, names):
        try:
            # Create remediation instance for every definition reference id.
            remediate_instance = Remediation(policy_assignment_id=assignment_id, policy_definition_reference_id=id, resource_discovery_mode="ReEvaluateCompliance")
            
            # Create the task at subscription level. Can use other methods for Manage Group and Resource Group.
            result = policy_insights_client.remediations.create_or_update_at_subscription(remediation_name=f"{name}-remediatetest", parameters=remediate_instance)
            
            # Because we are creating multiple at once, you need to wait for each remediation to complete before creating the next one.
            while result.provisioning_state != "Succeeded":
                print(f"Provisioning state: {result.provisioning_state}")
                print(f"Waiting for {result.id.split("/")[-1]} provisioning state to change...")
                time.sleep(60)  # Example: wait for 60 seconds before checking again
                result = policy_insights_client.remediations.get_at_subscription(remediation_name=f"{name}-remediatetest")
                print(f"Provisioning state changed to: {result.provisioning_state}")

                if result.provisioning_state == "Succeeded":
                    break  # Exit the while loop once the remediation task is successful

        except Exception as e:
            print(f"An error occurred: {e}")

    print("All remediation tasks completed.")
        

def main():
    """Run the remediation function"""
    remediation()


if __name__ == "__main__":
    main()




