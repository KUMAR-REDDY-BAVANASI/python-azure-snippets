from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.v2017_10_01.models import NetworkSecurityGroup
from azure.mgmt.network.v2017_10_01.models import SecurityRule
from decouple import config
import json

# Configure Credentials
client_id = config('AZURE_CLIENT_ID')
client_secret = config('AZURE_CLIENT_SECRET')
tenant = config('AZURE_TENANT_ID')

credentials = ServicePrincipalCredentials(
  client_id = client_id,
  secret = client_secret,
  tenant = tenant
)

# Retrieve subscription ID from environment variable.
subscription_id = config('SUBSCRIPTION_ID')


# Obtain the management object for networks
network_client = NetworkManagementClient(credentials, subscription_id)

# Parameters of rg and nsg
resource_group_name = "rgs"
nsg_name = "testnsg"

print("Creating network security group with rules....")
nsg=network_client.network_security_groups.create_or_update(
    resource_group_name,
    nsg_name, 
    NetworkSecurityGroup(
        location = "eastus",
        security_rules = [SecurityRule(
            name = "SSH From Home",
            description = "Rule01",
            source_address_prefix='*',
            destination_address_prefix='*',
            protocol = "Tcp",
            source_port_range="*",
            destination_port_range="22",
            access='Allow',
            direction='Inbound',
            priority = 1001
        )]
    )
)
nsg_result = nsg.result()
json_res = json.dumps(nsg_result.as_dict())
print(json_res)

