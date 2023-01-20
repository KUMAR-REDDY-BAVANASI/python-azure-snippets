from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from decouple import config
import json

def main():

    # Configure Credentials
    client_id = config('AZURE_CLIENT_ID')
    client_secret = config('AZURE_CLIENT_SECRET')
    tenant = config('AZURE_TENANT_ID')
    
    credentials = ServicePrincipalCredentials(
      client_id = client_id,
      secret = client_secret,
      tenant = tenant
    )
    
    resourceGroupName = config('resource_group_name')
    subscription_id = config('SUBSCRIPTION_ID')
    
    # Create Client
    resource_client = ResourceManagementClient(
      credentials,
      subscription_id
      )
    
    print("The authentications is successfull")

    # Azure Params 
    resourceGroupName = config("resource_group_name")
    subscription_id = config('SUBSCRIPTION_ID')

    # Create resource group
    rg_result = resource_client.resource_groups.create_or_update(
        resourceGroupName,
        {"location": "eastus"}
    )
    print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")
    json_res = json.dumps(rg_result.as_dict())
    print(json_res)

if __name__ == "__main__":
    main()
