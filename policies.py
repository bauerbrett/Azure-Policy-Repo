

policy_list = {}

#Policy to enable logging on Key Vaults.
key_policy = {
    "properties":  {
                       "displayName":  "",
                       "mode":  "All",
                       "description":  "This policy automatically deploys diagnostic settings to Key Vaults.",
                       "metadata":  {
                                        "category":  "Monitoring"
                                    },
                       "parameters":  {
                                          "profileName":  {
                                                              "type":  "String",
                                                              "metadata":  {
                                                                               "displayName":  "Profile Name for Config",
                                                                               "description":  "The profile name Azure Diagnostics"
                                                                           },
                                                               "defaultValue":  "Diag_to_Sentinel"
                                                          },
                                          "logAnalytics":  {
                                                               "type":  "string",
                                                               "metadata":  {
                                                                                "displayName":  "logAnalytics",
                                                                                "description":  "The target Log Analytics Workspace for Azure Diagnostics",
                                                                                "strongType":  "omsWorkspace"
                                                                            },
                                                                "defaultValue": "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/resourceGroups/azlabs/providers/Microsoft.OperationalInsights/workspaces/Sentinel-Test"
                                                           },
                                          "azureRegions":  {
                                                               "type":  "Array",
                                                               "metadata":  {
                                                                                "displayName":  "Allowed Locations",
                                                                                "description":  "The list of locations that can be specified when deploying resources",
                                                                                "strongType":  "location"
                                                                            },
                                                                "defaultValue": ['eastus']
                                                           },
                                          "metricsEnabled":  {
                                                                 "type":  "String",
                                                                 "metadata":  {
                                                                                  "displayName":  "Enable Metrics",
                                                                                  "description":  "Enable Metrics - True or False"
                                                                              },
                                                                 "allowedValues":  [
                                                                                       "True",
                                                                                       "False"
                                                                                   ],
                                                                 "defaultValue":  "False"
                                                             },
                                          "logsEnabled":  {
                                                              "type":  "String",
                                                              "metadata":  {
                                                                               "displayName":  "Enable Logs",
                                                                               "description":  "Enable Logs - True or False"
                                                                           },
                                                              "allowedValues":  [
                                                                                    "True",
                                                                                    "False"
                                                                                ],
                                                              "defaultValue":  "True"
                                                          }
                                      },
                       "policyRule":  {
                                          "if":  {
                                                     "allOf":  [
                                                                   {
                                                                       "field":  "type",
                                                                       "equals":  "Microsoft.KeyVault/vaults"
                                                                   },
                                                                   {
                                                                       "field":  "location",
                                                                       "in":  "[parameters('AzureRegions')]"
                                                                   }
                                                               ]
                                                 },
                                          "then":  {
                                                       "effect":  "deployIfNotExists",
                                                       "details":  {
                                                                       "type":  "Microsoft.Insights/diagnosticSettings",
                                                                       "existenceCondition":  {
                                                                                                  "allOf":  [
                                                                                                                {
                                                                                                                    "field":  "Microsoft.Insights/diagnosticSettings/logs.enabled",
                                                                                                                    "equals":  "[parameters('LogsEnabled')]"
                                                                                                                },
                                                                                                                {
                                                                                                                    "field":  "Microsoft.Insights/diagnosticSettings/metrics.enabled",
                                                                                                                    "equals":  "[parameters('MetricsEnabled')]"
                                                                                                                },
                                                                                                                {
                                                                                                                    "field":  "Microsoft.Insights/diagnosticSettings/workspaceId",
                                                                                                                    "equals":  "[parameters('logAnalytics')]"
                                                                                                                }
                                                                                                            ]
                                                                                              },
                                                                       "roleDefinitionIds":  [
                                                                                                 "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/providers/Microsoft.Authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293",
                                                                                                 "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/providers/Microsoft.Authorization/roleDefinitions/749f88d5-cbae-40b8-bcfc-e573ddc772fa"
                                                                                             ],
                                                                       "deployment":  {
                                                                                          "properties":  {
                                                                                                             "mode":  "incremental",
                                                                                                             "template":  {
                                                                                                                              "$schema":  "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                                                                                                                              "contentVersion":  "1.0.0.0",
                                                                                                                              "parameters":  {
                                                                                                                                                 "name":  {
                                                                                                                                                              "type":  "string"
                                                                                                                                                          },
                                                                                                                                                 "location":  {
                                                                                                                                                                  "type":  "string"
                                                                                                                                                              },
                                                                                                                                                 "logAnalytics":  {
                                                                                                                                                                      "type":  "string"
                                                                                                                                                                  },
                                                                                                                                                 "metricsEnabled":  {
                                                                                                                                                                        "type":  "string"
                                                                                                                                                                    },
                                                                                                                                                 "logsEnabled":  {
                                                                                                                                                                     "type":  "string"
                                                                                                                                                                 },
                                                                                                                                                 "profileName":  {
                                                                                                                                                                     "type":  "string"
                                                                                                                                                                 }
                                                                                                                                             },
                                                                                                                              "variables":  {

                                                                                                                                            },
                                                                                                                              "resources":  [
                                                                                                                                                {
                                                                                                                                                    "type":  "Microsoft.KeyVault/vaults/providers/diagnosticSettings",
                                                                                                                                                    "apiVersion":  "2017-05-01-preview",
                                                                                                                                                    "name":  "[concat(parameters('name'), '/', 'Microsoft.Insights/', parameters('profileName'))]",
                                                                                                                                                    "location":  "[parameters('location')]",
                                                                                                                                                    "properties":  {
                                                                                                                                                                       "workspaceId":  "[parameters('logAnalytics')]",
                                                                                                                                                                       "metrics":  [
                                                                                                                                                                                       {
                                                                                                                                                                                           "category":  "AllMetrics",
                                                                                                                                                                                           "enabled":  "[parameters('metricsEnabled')]",
                                                                                                                                                                                           "retentionPolicy":  {
                                                                                                                                                                                                                   "enabled":  False,
                                                                                                                                                                                                                   "days":  0
                                                                                                                                                                                                               }
                                                                                                                                                                                       }
                                                                                                                                                                                   ],
                                                                                                                                                                       "logs":  [
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AuditEvent",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzurePolicyEvaluationDetails",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    }
                                                                                                                                                                                ]
                                                                                                                                                                   }
                                                                                                                                                }
                                                                                                                                            ],
                                                                                                                              "outputs":  {
                                                                                                                                              "policy":  {
                                                                                                                                                             "type":  "string",
                                                                                                                                                             "value":  "[concat(parameters('logAnalytics'), 'configured for diagnostic logs for ', ': ', parameters('name'))]"
                                                                                                                                                         }
                                                                                                                                          }
                                                                                                                          },
                                                                                                             "parameters":  {
                                                                                                                                "logAnalytics":  {
                                                                                                                                                     "value":  "[parameters('logAnalytics')]"
                                                                                                                                                 },
                                                                                                                                "location":  {
                                                                                                                                                 "value":  "[field('location')]"
                                                                                                                                             },
                                                                                                                                "name":  {
                                                                                                                                             "value":  "[field('name')]"
                                                                                                                                         },
                                                                                                                                "metricsEnabled":  {
                                                                                                                                                       "value":  "[parameters('metricsEnabled')]"
                                                                                                                                                   },
                                                                                                                                "logsEnabled":  {
                                                                                                                                                    "value":  "[parameters('logsEnabled')]"
                                                                                                                                                },
                                                                                                                                "profileName":  {
                                                                                                                                                    "value":  "[parameters('profileName')]"
                                                                                                                                                }
                                                                                                                            }
                                                                                                         }
                                                                                      }
                                                                   }
                                                   }
                                      }
                   }
}

policy_list["Key_Vault_Policy"] = key_policy


storage_account_policy = {
  "properties": {
    "displayName": "Configure diagnostic settings for Blob Services to Log Analytics workspace",
    "policyType": "Custom",
    "mode": "All",
    "description": "Deploys the diagnostic settings for Blob Services to stream resource logs to a Log Analytics workspace when any blob Service which is missing this diagnostic settings is created or updated.",
    "metadata": {
      "category": "Storage",
      "version": "4.0.0"
    },
    "version": "4.0.0",
    "parameters": {
      "effect": {
        "type": "String",
        "metadata": {
          "displayName": "Effect",
          "description": "Enable or disable the execution of the policy"
        },
        "allowedValues": [
          "DeployIfNotExists",
          "AuditIfNotExists",
          "Disabled"
        ],
        "defaultValue": "DeployIfNotExists"
      },
      "profileName": {
        "type": "String",
        "metadata": {
          "displayName": "Profile name",
          "description": "The diagnostic settings profile name"
        },
        "defaultValue": "blobServicesDiagnosticsLogsToWorkspace"
      },
      "logAnalytics": {
        "type": "String",
        "metadata": {
          "displayName": "Log Analytics workspace",
          "description": "Select Log Analytics workspace from dropdown list. If this workspace is outside of the scope of the assignment you must manually grant 'Log Analytics Contributor' permissions (or similar) to the policy assignment's principal ID.",
          "strongType": "omsWorkspace",
          "assignPermissions": True
        },
        "defaultValue": "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/resourceGroups/azlabs/providers/Microsoft.OperationalInsights/workspaces/Sentinel-Test"
        
      },
      "metricsEnabled": {
        "type": "Boolean",
        "metadata": {
          "displayName": "Enable metrics",
          "description": "Whether to enable metrics stream to the Log Analytics workspace - True or False"
        },
        "allowedValues": [
          True,
          False
        ],
        "defaultValue": True
      },
      "logsEnabled": {
        "type": "Boolean",
        "metadata": {
          "displayName": "Enable logs",
          "description": "Whether to enable logs stream to the Log Analytics workspace - True or False"
        },
        "allowedValues": [
          True,
          False
        ],
        "defaultValue": True
      }
    },
    "policyRule": {
      "if": {
        "field": "type",
        "equals": "Microsoft.Storage/storageAccounts/blobServices"
      },
      "then": {
        "effect": "[parameters('effect')]",
        "details": {
          "type": "Microsoft.Insights/diagnosticSettings",
          "name": "[parameters('profileName')]",
          "existenceCondition": {
            "allOf": [
              {
                "field": "Microsoft.Insights/diagnosticSettings/logs.enabled",
                "equals": "[parameters('logsEnabled')]"
              },
              {
                "field": "Microsoft.Insights/diagnosticSettings/metrics.enabled",
                "equals": "[parameters('metricsEnabled')]"
              },
              {
                "field": "Microsoft.Insights/diagnosticSettings/workspaceId",
                "equals": "[parameters('logAnalytics')]"
              }
            ]
          },
          "roleDefinitionIds": [
            "/providers/microsoft.authorization/roleDefinitions/749f88d5-cbae-40b8-bcfc-e573ddc772fa",
            "/providers/microsoft.authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293"
          ],
          "deployment": {
            "properties": {
              "mode": "incremental",
              "template": {
                "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {
                  "resourceName": {
                    "type": "string"
                  },
                  "location": {
                    "type": "string"
                  },
                  "logAnalytics": {
                    "type": "string"
                  },
                  "metricsEnabled": {
                    "type": "bool"
                  },
                  "logsEnabled": {
                    "type": "bool"
                  },
                  "profileName": {
                    "type": "string"
                  }
                },
                "variables": {},
                "resources": [
                  {
                    "type": "Microsoft.Storage/storageAccounts/blobServices/providers/diagnosticSettings",
                    "apiVersion": "2021-05-01-preview",
                    "name": "[concat(parameters('resourceName'), '/', 'Microsoft.Insights/', parameters('profileName'))]",
                    "location": "[parameters('location')]",
                    "dependsOn": [],
                    "properties": {
                      "workspaceId": "[parameters('logAnalytics')]",
                      "metrics": [
                        {
                          "category": "AllMetrics",
                          "enabled": "[parameters('metricsEnabled')]"
                        }
                      ],
                      "logs": [
                        {
                          "category": "StorageRead",
                          "enabled": "[parameters('logsEnabled')]"
                        },
                        {
                          "category": "StorageWrite",
                          "enabled": "[parameters('logsEnabled')]"
                        },
                        {
                          "category": "StorageDelete",
                          "enabled": "[parameters('logsEnabled')]"
                        }
                      ]
                    }
                  }
                ],
                "outputs": {}
              },
              "parameters": {
                "location": {
                  "value": "[field('location')]"
                },
                "resourceName": {
                  "value": "[field('fullName')]"
                },
                "logAnalytics": {
                  "value": "[parameters('logAnalytics')]"
                },
                "metricsEnabled": {
                  "value": "[parameters('metricsEnabled')]"
                },
                "logsEnabled": {
                  "value": "[parameters('logsEnabled')]"
                },
                "profileName": {
                  "value": "[parameters('profileName')]"
                }
              }
            }
          }
        }
      }
    },
    "versions": [
      "4.0.0"
    ]
  },
  "id": "/providers/Microsoft.Authorization/policyDefinitions/b4fe1a3b-0715-4c6c-a5ea-ffc33cf823cb",
  "type": "Microsoft.Authorization/policyDefinitions",
  "name": "b4fe1a3b-0715-4c6c-a5ea-ffc33cf823cb"
}


policy_list["Storage_Account_Policy"] = storage_account_policy


recovery_vault_policy = {
    "properties":  {
                       "displayName":  "",
                       "mode":  "All",
                       "description":  "This policy automatically deploys diagnostic settings to .",
                       "metadata":  {
                                        "category":  "Monitoring"
                                    },
                       "parameters":  {
                                          "profileName":  {
                                                              "type":  "String",
                                                              "metadata":  {
                                                                               "displayName":  "Profile Name for Config",
                                                                               "description":  "The profile name Azure Diagnostics"
                                                                           },

                                                                "defaultValue":  "Diag_to_Sentinel"
                                                          },
                                          "logAnalytics":  {
                                                               "type":  "string",
                                                               "metadata":  {
                                                                                "displayName":  "logAnalytics",
                                                                                "description":  "The target Log Analytics Workspace for Azure Diagnostics",
                                                                                "strongType":  "omsWorkspace"
                                                                            },
                                                                "defaultValue": "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/resourceGroups/azlabs/providers/Microsoft.OperationalInsights/workspaces/Sentinel-Test"
                                                           },
                                          "azureRegions":  {
                                                               "type":  "Array",
                                                               "metadata":  {
                                                                                "displayName":  "Allowed Locations",
                                                                                "description":  "The list of locations that can be specified when deploying resources",
                                                                                "strongType":  "location"
                                                                            },
                                                                "defaultValue": ['eastus']
                                                           },
                                          "metricsEnabled":  {
                                                                 "type":  "String",
                                                                 "metadata":  {
                                                                                  "displayName":  "Enable Metrics",
                                                                                  "description":  "Enable Metrics - True or False"
                                                                              },
                                                                 "allowedValues":  [
                                                                                       "True",
                                                                                       "False"
                                                                                   ],
                                                                 "defaultValue":  "False"
                                                             },
                                          "logsEnabled":  {
                                                              "type":  "String",
                                                              "metadata":  {
                                                                               "displayName":  "Enable Logs",
                                                                               "description":  "Enable Logs - True or False"
                                                                           },
                                                              "allowedValues":  [
                                                                                    "True",
                                                                                    "False"
                                                                                ],
                                                              "defaultValue":  "True"
                                                          }
                                      },
                       "policyRule":  {
                                          "if":  {
                                                     "allOf":  [
                                                                   {
                                                                       "field":  "type",
                                                                       "equals":  "Microsoft.RecoveryServices/vaults"
                                                                   },
                                                                   {
                                                                       "field":  "location",
                                                                       "in":  "[parameters('AzureRegions')]"
                                                                   }
                                                               ]
                                                 },
                                          "then":  {
                                                       "effect":  "deployIfNotExists",
                                                       "details":  {
                                                                       "type":  "Microsoft.Insights/diagnosticSettings",
                                                                       "existenceCondition":  {
                                                                                                  "allOf":  [
                                                                                                                {
                                                                                                                    "field":  "Microsoft.Insights/diagnosticSettings/logs.enabled",
                                                                                                                    "equals":  "[parameters('LogsEnabled')]"
                                                                                                                },
                                                                                                                {
                                                                                                                    "field":  "Microsoft.Insights/diagnosticSettings/metrics.enabled",
                                                                                                                    "equals":  "[parameters('MetricsEnabled')]"
                                                                                                                },
                                                                                                                {
                                                                                                                    "field":  "Microsoft.Insights/diagnosticSettings/workspaceId",
                                                                                                                    "equals":  "[parameters('logAnalytics')]"
                                                                                                                }
                                                                                                            ]
                                                                                              },
                                                                       "roleDefinitionIds":  [
                                                                                                 "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/providers/Microsoft.Authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293",
                                                                                                 "/subscriptions/3b8667c6-8f75-42ea-b301-bf27c9db8674/providers/Microsoft.Authorization/roleDefinitions/749f88d5-cbae-40b8-bcfc-e573ddc772fa"
                                                                                             ],
                                                                       "deployment":  {
                                                                                          "properties":  {
                                                                                                             "mode":  "incremental",
                                                                                                             "template":  {
                                                                                                                              "$schema":  "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                                                                                                                              "contentVersion":  "1.0.0.0",
                                                                                                                              "parameters":  {
                                                                                                                                                 "name":  {
                                                                                                                                                              "type":  "string"
                                                                                                                                                          },
                                                                                                                                                 "location":  {
                                                                                                                                                                  "type":  "string"
                                                                                                                                                              },
                                                                                                                                                 "logAnalytics":  {
                                                                                                                                                                      "type":  "string"
                                                                                                                                                                  },
                                                                                                                                                 "metricsEnabled":  {
                                                                                                                                                                        "type":  "string"
                                                                                                                                                                    },
                                                                                                                                                 "logsEnabled":  {
                                                                                                                                                                     "type":  "string"
                                                                                                                                                                 },
                                                                                                                                                 "profileName":  {
                                                                                                                                                                     "type":  "string"
                                                                                                                                                                 }
                                                                                                                                             },
                                                                                                                              "variables":  {

                                                                                                                                            },
                                                                                                                              "resources":  [
                                                                                                                                                {
                                                                                                                                                    "type":  "Microsoft.RecoveryServices/vaults/providers/diagnosticSettings",
                                                                                                                                                    "apiVersion":  "2017-05-01-preview",
                                                                                                                                                    "name":  "[concat(parameters('name'), '/', 'Microsoft.Insights/', parameters('profileName'))]",
                                                                                                                                                    "location":  "[parameters('location')]",
                                                                                                                                                    "properties":  {
                                                                                                                                                                       "workspaceId":  "[parameters('logAnalytics')]",
                                                                                                                                                                       "metrics":  [
                                                                                                                                                                                       {
                                                                                                                                                                                           "category":  "AllMetrics",
                                                                                                                                                                                           "enabled":  "[parameters('metricsEnabled')]",
                                                                                                                                                                                           "retentionPolicy":  {
                                                                                                                                                                                                                   "enabled":  False,
                                                                                                                                                                                                                   "days":  0
                                                                                                                                                                                                               }
                                                                                                                                                                                       }
                                                                                                                                                                                   ],
                                                                                                                                                                       "logs":  [
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureBackupReport",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "CoreAzureBackup",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AddonAzureBackupJobs",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AddonAzureBackupAlerts",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AddonAzureBackupPolicy",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AddonAzureBackupStorage",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AddonAzureBackupProtectedInstance",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryJobs",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryEvents",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryReplicatedItems",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryReplicationStats",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryRecoveryPoints",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryReplicationDataUploadRate",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureSiteRecoveryProtectedDiskDataChurn",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "ASRReplicatedItems",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    },
                                                                                                                                                                                    {
                                                                                                                                                                                        "category":  "AzureBackupOperations",
                                                                                                                                                                                        "enabled":  "[parameters('logsEnabled')]"
                                                                                                                                                                                    }
                                                                                                                                                                                ]
                                                                                                                                                                   }
                                                                                                                                                }
                                                                                                                                            ],
                                                                                                                              "outputs":  {
                                                                                                                                              "policy":  {
                                                                                                                                                             "type":  "string",
                                                                                                                                                             "value":  "[concat(parameters('logAnalytics'), 'configured for diagnostic logs for ', ': ', parameters('name'))]"
                                                                                                                                                         }
                                                                                                                                          }
                                                                                                                          },
                                                                                                             "parameters":  {
                                                                                                                                "logAnalytics":  {
                                                                                                                                                     "value":  "[parameters('logAnalytics')]"
                                                                                                                                                 },
                                                                                                                                "location":  {
                                                                                                                                                 "value":  "[field('location')]"
                                                                                                                                             },
                                                                                                                                "name":  {
                                                                                                                                             "value":  "[field('name')]"
                                                                                                                                         },
                                                                                                                                "metricsEnabled":  {
                                                                                                                                                       "value":  "[parameters('metricsEnabled')]"
                                                                                                                                                   },
                                                                                                                                "logsEnabled":  {
                                                                                                                                                    "value":  "[parameters('logsEnabled')]"
                                                                                                                                                },
                                                                                                                                "profileName":  {
                                                                                                                                                    "value":  "[parameters('profileName')]"
                                                                                                                                                }
                                                                                                                            }
                                                                                                         }
                                                                                      }
                                                                   }
                                                   }
                                      }
                   }
}


policy_list["Recovery_Vault_Policy"] = recovery_vault_policy
