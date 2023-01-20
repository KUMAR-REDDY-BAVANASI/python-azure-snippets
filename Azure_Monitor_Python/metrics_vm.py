from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorClient
from decouple import config
import datetime

# Configure Credentials
client_id = config('AZURE_CLIENT_ID')
client_secret = config('AZURE_CLIENT_SECRET')
tenant = config('AZURE_TENANT_ID')

credentials = ClientSecretCredential(
  client_id = client_id,
  client_secret = client_secret,
  tenant_id = tenant
)  
SUBSCRIPTION_ID = config('SUBSCRIPTION_ID')

# Create client
client = MonitorClient(
    credential=credentials,
    subscription_id=SUBSCRIPTION_ID
)

# Azure Resources Params
SUBSCRIPTION_ID = config('SUBSCRIPTION_ID')
resource_group_name = config('resource_group_name')
vm_name = "AnsiblePoC"

# Get the ARM id of your resource. You might chose to do a "get"
resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(SUBSCRIPTION_ID, resource_group_name, vm_name)


# You can get the available metrics of this specific resource
for metric in client.metric_definitions.list(resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))


# Get CPU total of yesterday for this VM, by hour
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

metrics_data = client.metrics.list(
    resource_id,
    timespan="{}/{}".format(yesterday, today),
    interval='PT1H',
    metricnames='Percentage CPU',
    aggregation='average'
)

for item in metrics_data.value:
    print("{} ({})".format(item.name.localized_value, item.unit))
    for timeserie in item.timeseries:
        for data in timeserie.data:
            # azure.mgmt.monitor.models.MetricData
            print("{}: {}".format(data.time_stamp, data.average))
