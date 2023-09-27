# Dapr Azure queue with Key Vault

Example of how to setup a Dapr component that uses azure queue binding 
to send messages to an Azure queue.

## Setup components

The azure queue component should not reference the Azure storage keys.
This can be done by referencing an Azure KeyVault component:

components/azurequeue.yaml

```
  apiVersion: dapr.io/v1alpha1
  kind: Component
  metadata:
    name: azurequeue
  spec:
    type: bindings.azure.storagequeues
    version: v1
    metadata:
    - name: accountName
      value: "rkacrstg"
    - name: accountKey
      secretKeyRef:
        name: storagekey
        key: storagekey
    - name: queueName
      value: "daprqueue"
  auth:
    secretStore: daprkeyvault
```
components/keyvault.yaml

```
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: daprkeyvault
spec:
  type: secretstores.azure.keyvault
  version: v1
  metadata:
  - name: vaultName # Required don't rename it must be vaultName - https://docs.dapr.io/reference/components-reference/supported-secret-stores/azure-keyvault/
    value: "rk-aca-kv"
  - name: azureEnvironment # Optional, defaults to AZUREPUBLICCLOUD
    value: "AZUREPUBLICCLOUD"
  # See authentication section below for all options
  - name: azureTenantId
    value: "7638c56b-088d-4428-bbba-b28cc2fd26fa"
  - name: azureClientId
    value: "d5f775f4-13be-4b6b-aad7-c52e5fd9bd0d"
  - name: azureClientSecret
    value: "******"
```

## Test the component

To test run as a blank app from the components folder or pass in the full path.

```
 dapr run --app-id myqueueapp --dapr-http-port 3500 --resources-path .

```

Use curl to test the message is enqueued:

```
curl -X POST http://localhost:3500/v1.0/bindings/azurequeue \
  -H "Content-Type: application/json" \
  -d '{
        "data": {
          "message": "A dapr storage queue configured"
        },
        "metadata": {
          "ttlInSeconds": "60"
        },
        "operation": "create"
      }'         

```
If successful there should be no error written to stdout.

## Test the component using python client sdk

To run this use the following command:

```
dapr run --app-id myqueueapp   --resources-path ./components -- python3 createmessage-dapr.py

```
Key points pass the python script at the end using:

```
-- python3 createmessage-dapr.py
```

## Test queue input binding with Python flask

To test the equivalent input binding with Azure queue configure the following component:

```
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: processmessage
spec:
  type: bindings.azure.storagequeues
  version: v1
  metadata:
  - name: accountName
    value: "rkacrstg"
  - name: accountKey
    secretKeyRef:
      name: storagekey
      key: storagekey
  - name: queueName
    value: "daprqueue"
auth:
  secretStore: daprkeyvault
```

Then create a simple python app listening on endpoint /processmessage 

```
from flask import Flask, request
app = Flask(__name__)

@app.route("/processmessage", methods=['POST'])
def incoming():
    print(request.data, flush=True)

    return "Azure queue message Processed!"
```
The flask route must match metadata: name property on the azurequeue-in.yaml

Then start Dapr up:

```
dapr run --app-id queuetrigger  --app-port=5000 --dapr-http-port 3500 --resources-path ./components -- flask --app receivemessage.py run
```
This will create a trigger on the queue everyime a message is posted.

You can test this by running the following dapr:

```
dapr run --app-id queueout   --resources-path ./components -- python3 createmessage-dapr.py

```