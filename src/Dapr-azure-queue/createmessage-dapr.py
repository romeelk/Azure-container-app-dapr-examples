from dapr.clients import DaprClient
import json

message_body = "{\"message\": \"A dapr storage queue configured\"}"

message_data = {
   "data": message_body,
   "operation": "create",
   "metadata": {
       "ttlInSeconds": "60"
   }
}
queue_name = "azurequeue"
with DaprClient() as d:
    d.invoke_binding(queue_name, 'create', json.dumps(message_data))
    print(f"sent message to {queue_name}")  