locals {
  tags = {
    "environment" = "dev"
    "author" = "Romeel Khan"
    "iac" = "terraform - azapi"
  }
}

resource "azurerm_resource_group" "rg" {
  name      = "rg-aca-scalerule"
  location  = var.location
  tags      = local.tags
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-aca-scalerule"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
  retention_in_days   = 90
  tags                = local.tags
}


resource "azapi_resource" "acappenv" {
  type = "Microsoft.App/managedEnvironments@2023-05-01"
  name = "aca-env-scalerule"
  tags = local.tags
  location = azurerm_resource_group.rg.location
  parent_id = azurerm_resource_group.rg.id
  body = jsonencode({
    properties = {
      appLogsConfiguration = {
        destination = "log-analytics"
        logAnalyticsConfiguration = {
          customerId = azurerm_log_analytics_workspace.law.workspace_id
          sharedKey  = azurerm_log_analytics_workspace.law.primary_shared_key
        }
      }
    }
  })
}

resource "azapi_resource" "producer_container_app" {
  name      = "aca-app-httpscalerule"
  location  = var.location
  tags = local.tags
  parent_id = azurerm_resource_group.rg.id
  type      = "Microsoft.App/containerApps@2022-03-01"
  body = jsonencode({
    properties = {
      managedEnvironmentId = azapi_resource.acappenv.id
      configuration = {
        ingress = {
          targetPort = 80
          external   = true
        }
      },
      template = {
        containers = [
          {
            image = "nginx"
            name  = "nginxcontainerapp",
          }
        ]
        scale = {
          minReplicas = 1
          maxReplicas = 4
          rules = [
            {
              http = {
                metadata = {
                  concurrentRequests = "2"
                }
              }
              name = "http-rule" 
            }
          ]
        
        }
      }
    }
  })
}
