# Import the needed credential and management objects from the libraries.
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql.models import *
from decouple import config
import json

print(f"Provisioning a mysql server...some operations might take a minute or two.")

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


# Step 1: Provision a resource group

# Obtain the management object for resources, using the credentials from the CLI login.
resource_client = ResourceManagementClient(credentials, subscription_id)

# Constants we need in multiple places: the resource group name and the region
RESOURCE_GROUP_NAME = "mysql_db_resgroup"
LOCATION = "eastus"

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
    {
        "location": LOCATION
    }
)

print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")


# Step 2: Provision a mysql database server
# Parameters for mysql database

RESOURCE_GROUP = "mysql_db_resgroup"
SERVER = "Testing-db5483"
ADMIN_USER = "admin5483"
ADMIN_PASSWORD = "hiue51afDHwd5hSBdw4HJVD"
LOCATION = "eastus"


# Obtain the management object for resources, using the credentials from the CLI login.
client = MySQLManagementClient(credentials, subscription_id)

print(f"Provisioning a mysql server...some operations might take a minute or two.")

# Mysql_db server creation 
server_creation_poller = client.servers.create(
    RESOURCE_GROUP,
    SERVER,
    ServerForCreate(
        properties=ServerPropertiesForDefaultCreate(
            administrator_login=ADMIN_USER,
            administrator_login_password=ADMIN_PASSWORD,
            version="5.7",
            storage_profile=StorageProfile(
                storage_mb=51200
            )
        ),
        location=LOCATION,
        sku=Sku(
            name="GP_Gen5_2"
        )
    )
)

server = server_creation_poller.result()
json_res = json.dumps(server.as_dict())
print(json_res)


# Step 3: Provision a firewall rule to allow the local workstation to connect

# Open access to this server for IPs
rule_creation_poller = client.firewall_rules.create_or_update(
    RESOURCE_GROUP,
    SERVER,
    "allow_ip",  # Custom firewall rule name
    "0.0.0.0",  # Start ip range
    "255.255.255.255"  # End ip range
)

firewall_rule = rule_creation_poller.result()
print(f"Provisioned firewall rule {firewall_rule.name}")

json_res = json.dumps(firewall_rule.as_dict())
print(json_res)