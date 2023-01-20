from azure.mgmt.trafficmanager import TrafficManagerManagementClient
from azure.mgmt.trafficmanager.models import EndpointStatus, Endpoint
from azure.common.credentials import ServicePrincipalCredentials
from decouple import config


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
tm_client = TrafficManagerManagementClient(
  credentials,
  subscription_id
  )

print("The authentications is successfull")

# define endpoint
param = Endpoint(
    # my target resource is Virtual Machine
    target_resource_id='/subscriptions/176f4009-62de-4f59-aaee-fed1efdf0a10/resourceGroups/MyResourceGroup/providers/Microsoft.Network/publicIPAddresses/DEMO-VM-ip',
    endpoint_status=EndpointStatus.enabled
)
result = tm_client.endpoints.create_or_update(
    resource_group_name='MyResourceGroup',
    profile_name='cloudkumar',
    endpoint_type='AzureEndpoints',
    endpoint_name='mypoint',
    parameters=param)
print(result.name)

