from decouple import config
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.dns import DnsManagementClient

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
zone = dns_client.zones.create_or_update(
         resourceGroupName,
        'cloudkumar.site',
        {
            'zone_type': 'Public', # or Private
                'location': 'global'
        }
)
print("""Create DNS Zone
               NAME:""", zone.name)




















'''
# Get the 'A' Record

get_record = dns_client.record_sets.get(
        'MyResourceGroup',
        'cloudkumar.site',
        'bos',
        'A'
)
print("""Get Record Sets
               IPV4_Address:""", get_record.arecords[0].ipv4_address)



# Update the A record

update_record_set = dns_client.record_sets.create_or_update(
	'MyResourceGroup',
	'cloudkumar.site',
	'bos',
	'A',
	{
			"ttl": 60,
			"arecords": [
				{
				"ipv4_address": "1.2.3.4"
				}
			]
	}
)
print("""Update Record Set
               NAME:""", update_record_set.arecords[0].ipv4_address)


# Delete Record Sets
delete_records = dns_client.record_sets.delete(
	'MyResourceGroup',
	'cloudkumar.site',
    'stg',
    'A'
)
print("""Deleted Record Set
               NAME:""", deleted_record.arecords[0].ipv4_address)


# Get the 'A' Record
deleted_record = dns_client.record_sets.get(
        'MyResourceGroup',
        'cloudkumar.site',
        'stg',
        'A'
)

print("""Get Record Sets
               IPV4_Address:""", res.arecords[0].ipv4_address)
'''









