from decouple import config
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.dns.models import Zone

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
dns_client = DnsManagementClient(
  credentials,
  subscription_id
  )

print("The authentications is successfull")


# Create 'A' Record Set With Alias Azure Resource Azure Traffic Manager

record_set = dns_client.record_sets.create_or_update(
	'MyResourceGroup',
	'cloudkumar.site',
	'bos',
	'CNAME',
	{
		"ttl": 60,
		"target_resource": {
			"id": "/subscriptions/176f4009-62de-4f59-aaee-fed1efdf0a10/resourcegroups/MyResourceGroup/providers/Microsoft.Network/trafficmanagerprofiles/cloudkumar",
		}
	}
)

print("""Create A recordset with alias 
               target resource(Traffic Manager Profile):""", record_set.name)
