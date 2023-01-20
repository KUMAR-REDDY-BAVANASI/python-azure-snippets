from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from decouple import config
import json


# Azure Datacenter
LOCATION = 'eastus'

# Resource Group
GROUP_NAME = 'rgs2'


# Load balancer
PUBLIC_IP_NAME = 'azure-sample-publicip'
LB_NAME = 'azure-sample-loadbalancer'
FIP_NAME = 'azure-sample-frontendipname'
ADDRESS_POOL_NAME = 'azure-sample-addr-pool'
PROBE_NAME = 'azure-sample-probe'
LB_RULE_NAME = 'azure-sample-lb-rule'

def run_example():

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
    resource_client = ResourceManagementClient(credentials, subscription_id)
    
    # Create Resource group
    print('Create Resource Group')
    rg_result = resource_client.resource_groups.create_or_update(
        GROUP_NAME, 
        {
            'location': LOCATION
        }
    )
    print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")
    
    # Create PublicIP
    print('Create Public IP')
    public_ip_parameters = {
        'location': LOCATION,
        'public_ip_allocation_method': 'static',
        # 'dns_settings': {
        #     'domain_name_label': DOMAIN_LABEL_NAME
        # },
        'idle_timeout_in_minutes': 4
    }
    publicip_creation = network_client.public_ip_addresses.create_or_update(
        GROUP_NAME,
        PUBLIC_IP_NAME,
        public_ip_parameters
    )
    public_ip_info = publicip_creation.result()
    json_res = json.dumps(public_ip_info.as_dict())
    print(json_res)
    
    print(f"Provisioned Public Ip {public_ip_info.name}")
    
    # Building a FrontEndIpPool
    print('Create FrontEndIpPool configuration')
    frontend_ip = [{
        'name': FIP_NAME,
        'private_ip_allocation_method': 'Dynamic',
        'public_ip_address': {
            'id': public_ip_info.id
        }
    }]
    # Building a BackEnd address pool
    print('Create BackEndAddressPool configuration')
    backend_pools = [{
        'name': ADDRESS_POOL_NAME
    }]
    # Building a HealthProbe
    print('Create HealthProbe configuration')
    health_probes = [{
        'name': PROBE_NAME,
        'protocol': 'Http',
        'port': 80,
        'interval_in_seconds': 15,
        'number_of_probes': 4,
        'request_path': '/'
    }]
    # Building a LoadBalancer rule
    print('Create LoadBalancerRule configuration')
    load_balancing_rules = [{
        'name': LB_RULE_NAME,
        'protocol': 'tcp',
        'frontend_port': 80,
        'backend_port': 80,
        'idle_timeout_in_minutes': 4,
        'enable_floating_ip': False,
        'load_distribution': 'Default',
        'frontend_ip_configuration': {
            'id': construct_fip_id(subscription_id)
        },
        'backend_address_pool': {
            'id': construct_bap_id(subscription_id)
        },
        'probe': {
            'id': construct_probe_id(subscription_id)
        }
    }]
    
    # Creating Load Balancer
    print('Creating Load Balancer')
    lb_creation = network_client.load_balancers.create_or_update(
        GROUP_NAME,
        LB_NAME,
        {
            'location': LOCATION,
            'frontend_ip_configurations': frontend_ip,
            'backend_address_pools': backend_pools,
            'probes': health_probes,
            'load_balancing_rules': load_balancing_rules,
        }
    )
    lb_info = lb_creation.result()
    json_res = json.dumps(lb_info.as_dict())
    print(json_res)

    print(f"Provisioned load balancer {lb_info.name}")


    
def construct_fip_id(subscription_id):
    """Build the future FrontEndId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/frontendIPConfigurations/{}').format(
                subscription_id, GROUP_NAME, LB_NAME, FIP_NAME
    )


def construct_bap_id(subscription_id):
    """Build the future BackEndId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/backendAddressPools/{}').format(
                subscription_id, GROUP_NAME, LB_NAME, ADDRESS_POOL_NAME
    )


def construct_probe_id(subscription_id):
    """Build the future ProbeId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/probes/{}').format(
                subscription_id, GROUP_NAME, LB_NAME, PROBE_NAME
    )
    
if __name__ == "__main__":
    run_example()