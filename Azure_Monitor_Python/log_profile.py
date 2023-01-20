from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.storage import StorageManagementClient
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
    storage_client = StorageManagementClient(
        credential=credentials,
        subscription_id=SUBSCRIPTION_ID
    )     

    # Azure Params 
    resource_group_name = config("resource_group_name")
    SUBSCRIPTION_ID = config('SUBSCRIPTION_ID')
    LOGPROFILE_NAME = "logprofilexx"
    STORAGE_ACCOUNT_NAME = "storageaccountxxy"

    # Create Storage
    storage_account = storage_client.storage_accounts.begin_create(
        resource_group_name,
        STORAGE_ACCOUNT_NAME,
        {
            "sku":{
                "name": "Standard_LRS"
            },
            "kind": "Storage",
            "location": "eastus",
            "enable_https_traffic_only": True
        }
    ).result()

    # Create log profile
    log_profile = monitor_client.log_profiles.create_or_update(
        LOGPROFILE_NAME,
        {
          "location": "",
          "locations": [
            "global"
          ],
          "categories": [
            "Write",
            "Delete",
            "Action"
          ],
          "retention_policy": {
            "enabled": True,
            "days": "3"
          },
          "storage_account_id": storage_account.id,
        }
    )
    print("Create log profile:\n{}".format(log_profile))

if __name__ == "__main__":
    main()
