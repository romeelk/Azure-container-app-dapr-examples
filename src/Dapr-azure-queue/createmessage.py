import requests
import json
message_body = "{\"message\": \"A dapr storage queue configured\"}"
message_data = {
   "data": message_body,
   "operation": "create",
   "metadata": {
       "ttlInSeconds": "60"
   }
}

response = requests.post("http://localhost:3500/v1.0/bindings/azurequeue", json.dumps(message_data))

print("Message sent to Azure queue")