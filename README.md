This is a python script to deploy an Azure Policy initiative. The policies.py file has the policy definitions inside a dictionary. To create your own policy definitions you need to copy and paste them into this file and make sure you add them to the dictionary. The deploy-policy script imports the policy dictionary and makes the initiative with the definitions in the dictionary.

The script also assigns roles to a managed identity and completes remediation tasks. Depending on your policy definitions you might need to add the roles through the definition or in the script. All you need is the role definition id, if you have it you can add it to the roles [] list. 

The remediation task are made to revaluate compliance because of this the script needs to wait until the remediation task is created to create the next task.

