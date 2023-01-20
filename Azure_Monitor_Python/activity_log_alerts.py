from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorClient
from decouple import config

# Azure Params
def main():
    # Configure Credentials
    client_id = config('AZURE_CLIENT_ID')
    client_secret = config('AZURE_CLIENT_SECRET')
    tenant = config('AZURE_TENANT_ID')
    
    credentials = ClientSecretCredential(
      client_id = client_id,
      client_secret = client_secret,
      tenant_id = tenant
    )  
    SUBSCRIPTION_ID = config('SUBSCRIPTION_ID')

    # Create client
    monitor_client = MonitorClient(
        credential=credentials,
        subscription_id=SUBSCRIPTION_ID
    )
     
    # Azure Params 
    resource_group_name = config("resource_group_name")
    ACTIVITY_LOG_ALERT_NAME = "Logx"
    ACTION_GROUP_NAME = "Fire_Group"


    # Get the ARM id of your ActionGroupId. You might chose to do a "get"
    action_group_id = (
    "/subscriptions/02ac19d2-71ae-471d-b697-97daef2db017/"
    "resourceGroups/Kumar_Testing/"
    "providers/microsoft.insights/actiongroups/Fire_Group"
    ).format(SUBSCRIPTION_ID, resource_group_name, ACTION_GROUP_NAME)

    ACTION_GROUP_URI = action_group_id
    print(ACTION_GROUP_URI)

    # Get the ARM id of your resource. You might chose to do a "get"
    resource_id = (
    "/subscriptions/02ac19d2-71ae-471d-b697-97daef2db017"
    ).format(SUBSCRIPTION_ID)

    RESOURCE_URI = resource_id
    print(RESOURCE_URI)

    # Create activity log alert
    log_alert = monitor_client.activity_log_alerts.create_or_update(
        resource_group_name,
        ACTIVITY_LOG_ALERT_NAME,
        {
          "location": "Global",
          "scopes": [
            RESOURCE_URI
          ],
          "enabled": True,
          "condition": {
            "all_of": [
              {
                "field": "category",
                "equals": "Administrative"
              },
              {
                "field": "level",
                "equals": "Informational"
              }
            ]
          },
          "actions": {
            "action_groups": [
              {
              "actionGroupId": ACTION_GROUP_URI
              }
            ]
          },
          "description": "Sample activity log alert description"
        }
    )
    print("Create activity log alert:\n{}".format(log_alert))

if __name__ == "__main__":
    main()
