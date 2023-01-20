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


#create profile
result = tm_client.profiles.create_or_update(

  resource_group_name='MyResourceGroup',
  profile_name='dev',
  parameters={
    "profileStatus": "Enabled",
    "trafficRoutingMethod": "Performance",
    "location": "global",
    "dnsConfig": {
      "relativeName": "Priority",
      "ttl": 35
    },
    "monitorConfig": {
      "protocol": "HTTP",
      "port": 80,
      "path": "/"
    }
}
)
print(result.name)
