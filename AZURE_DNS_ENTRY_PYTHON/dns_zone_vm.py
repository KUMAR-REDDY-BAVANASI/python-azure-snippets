from decouple import config
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.dns.models import Zone,RecordSet

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


# Create DNS Zone
params=Zone(
	zone_type='Public', # or Private
	location='global'
)

zone = dns_client.zones.create_or_update(
	resourceGroupName,
	zone_name='cloudkumar.site',
	parameters=params)

print("""Create DNS Zone
               NAME:""", zone.name)



# Create 'A' Record Set Pointing to Virtual Machine

params1=RecordSet(
	ttl=60,
    arecords=[
       {
		   'ipv4_address':'20.55.88.177'
       }
	]
)

record_set = dns_client.record_sets.create_or_update(
	resourceGroupName,
	zone_name='cloudkumar.site',
	relative_record_set_name='bos1',
	record_type='A',
	parameters=params
)

print("The ID of the record set:	", record_set.id)

print("""Create Record Set
               NAME:""", record_set.name)

print("The type of the record set:	", record_set.type)

print("Fully qualified domain name of the record set:	", record_set.fqdn)

print("Provisioning State of the record set:	", record_set.provisioning_state)

