from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.v2017_10_01.models import NetworkSecurityGroup
from azure.mgmt.network.v2017_10_01.models import SecurityRule
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

# Retrieve subscription ID from environment variable.
subscription_id = config('SUBSCRIPTION_ID')


# Obtain the management object for networks
network_client = NetworkManagementClient(credentials, subscription_id)

# Parameters of rg and nsg
resource_group_name = "PythonAzureExample-VM-rg"
nsg_name = "testnsg"

parameters = NetworkSecurityGroup()
parameters.id= "/subscriptions/02ac19d2-71ae-471d-b697-97daef2db017/resourceGroups/PythonAzureExample-VM-rg/providers/Microsoft.Network/networkSecurityGroups/testnsg/defaultSecurityRules/testnsg"
parameters.location = 'eastus'

parameters.security_rules = [SecurityRule(protocol='Tcp', source_address_prefix='*',
                              source_port_range="*", destination_port_range="", priority=100,
                              destination_address_prefix='*', access='Allow', direction='Inbound')]


nsg=network_client.network_security_groups.create_or_update(resource_group_name, "testnsg", parameters)
print(nsg.result().as_dict())
