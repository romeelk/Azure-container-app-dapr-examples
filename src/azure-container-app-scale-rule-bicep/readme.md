# Deploying Azure container app with bicep

This following example deploys a bicep template:

```
export RESOURCE_GROUP="rga-acapp-bicep"
export CONTAINERAPPS_ENVIRONMENT="acappenvhttpscale"
export LOCATION="uksouth"

az group create -n $RESOURCE_GROUP -l $LOCATION

az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file ./main.bicep \
  --parameters \
    environment_name="$CONTAINERAPPS_ENVIRONMENT" \
    location="$LOCATION" \
```

