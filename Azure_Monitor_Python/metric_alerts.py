from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorClient
from decouple import config

def main():
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
    monitor_client = MonitorClient(
        credential=credentials,
        subscription_id=SUBSCRIPTION_ID
    )
     
    # Azure Params 
    resource_group_name = config("resource_group_name")
    ACTION_GROUP_NAME = "Fire_Group"
    METRIC_ALERT_NAME = "High_CPU_60"
    VM_NAME = "AnsiblePoC"

  # Get the ARM id of your resource. You might chose to do a "get"
    resource_id = (
    "/subscriptions/02ac19d2-71ae-471d-b697-97daef2db017/"
    "resourceGroups/Kumar_Testing/"
    "providers/Microsoft.Compute/virtualMachines/AnsiblePoC"
    ).format(SUBSCRIPTION_ID, resource_group_name, VM_NAME)

    RESOURCE_URI = resource_id
    print(RESOURCE_URI)

  # Get the ARM id of your Actiongroup. You might chose to do a "get"
    action_group_id = (
    "/subscriptions/02ac19d2-71ae-471d-b697-97daef2db017/"
    "resourceGroups/Kumar_Testing/"
    "providers/microsoft.insights/actiongroups/Fire_Group"
    ).format(SUBSCRIPTION_ID, resource_group_name, ACTION_GROUP_NAME)

    ACTION_GROUP_URI = action_group_id
    print(ACTION_GROUP_URI)

    # Create metric alert
    metric_alert = monitor_client.metric_alerts.create_or_update(
        resource_group_name,
        METRIC_ALERT_NAME,
        {
          "location": "global",
          "description": "This is the description of the rule1",
          "severity": "3",
          "enabled": True,
          "scopes": [
            RESOURCE_URI
          ],
          "evaluation_frequency": "PT1M",
          "window_size": "PT15M",
          "target_resource_type": "Microsoft.Compute/virtualMachines",
          "target_resource_region": "eastus",
          "criteria": {
            "odata.type": "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria",
            "all_of": [
              {
                "criterion_type": "StaticThresholdCriterion",
                "name": "High_CPU_80",
                "metric_name": "Percentage CPU",
                "metric_namespace": "microsoft.compute/virtualmachines",
                "operator": "GreaterThan",
                "time_aggregation": "Average",
                "dimensions": [],
                "threshold": "60",
                "failing_periods": {
                  "number_of_evaluation_periods": "4",
                  "min_failing_periods_to_alert": "4"
                },
              }
            ]
          },
          "auto_mitigate": False,
          "actions": [
            {
              "actionGroupId": ACTION_GROUP_URI
            },
          ]
        }
    )
    print("Create metric alert:\n{}".format(metric_alert))

if __name__ == "__main__":
    main()
