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
resource_group_name = config("resource_group_name")
aks_name = "bos-dev-aks"

# Get the ARM id of your resource. You might chose to do a "get"
resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.ContainerService/managedClusters/{}"
).format(SUBSCRIPTION_ID, resource_group_name, aks_name)

# You can get the available metrics of this specific resource
for metric in client.metric_definitions.list(resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))

# Get Number of pods by phase  of last 12 hours for this AKS Cluster, by half an hour
today = datetime.datetime.now()
nexttime = today - datetime.timedelta(hours=12)

query_timespan = "{}/{}".format(nexttime, today - datetime.timedelta(hours=0))

print(query_timespan)

metrics_data = client.metrics.list(
    resource_id,
    timespan=query_timespan,
    interval='PT30M',
    metricnames='storage_limit',
    aggregation='average'
)

for item in metrics_data.value:
    print("{} ({})".format(item.name.localized_value, item.unit))
    for timeserie in item.timeseries:
        for data in timeserie.data:
            print("{}: {}".format(data.time_stamp, data.average))
