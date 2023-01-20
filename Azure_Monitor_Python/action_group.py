from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorClient
from decouple import config

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
    ACTION_GROUP_NAME = "Fire_Group"
    
    # Create action group
    action_group = monitor_client.action_groups.create_or_update(
        resource_group_name,
        ACTION_GROUP_NAME,
        {
          "location": "Global",
          "group_short_name": "Fire_Group",
          "enabled": True,
          "email_receivers": [
            {
              "name": "Kumar's email",
              "email_address": "kumar.b@bosframework.com",
              "use_common_alert_schema": False
            }
          ],
          "sms_receivers": [
            {
              "name": "Kumar's mobile",
              "country_code": "91",
              "phone_number": "8106808559"
            }
          ]
        }
    )
    print("Create action group:\n{}".format(action_group))


if __name__ == "__main__":
    main()
