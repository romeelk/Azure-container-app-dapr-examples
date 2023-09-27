## Dapr secret store example


# Define your component

Dapr components are configured as yaml files

```
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: my-secret-store
  namespace: default
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: ./app-secrets.json
  - name: nestedSeparator
    value: ":"
```


The aboe yaml defines a local secret that points to an app-secrets.json file

```
{
    "app-secret": "my app secret"
}
```

# Run your dapr component

To run configure your component simply run the following command to 
start an empty dapr app and sidecard. Make sure you are in the component
folder. Int his case it is ecret-store-component.

```
dapr run --app-id myapp --dapr-http-port 3500 --resources-path .
```

You can also pass the absolute path in the parameter --resources-path

# Access your secret over Http via the Dapr side car process

Once the app has started Dapr creates a side car component 

```
curl http://localhost:3500/v1.0/secrets/my-secret-store/app-secret

```

