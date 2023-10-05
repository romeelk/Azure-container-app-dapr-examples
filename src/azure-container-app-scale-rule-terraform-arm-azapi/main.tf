locals {
  tags = {
    "environment" = "dev"
    "author" = "Romeel Khan"
    "iac" = "azapi"
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


resource "azurerm_container_app_environment" "app_env" {
  name                       = "aca-env-scalerule"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}
resource "azurerm_container_app" "app_http_scale" {
  name                         = "aca-app-httpscalerule"
  container_app_environment_id = azurerm_container_app_environment.app_env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = "examplecontainerapp"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
    # http_scale_rule {
    #   name = "httpscalerule"
    #   concurrent_requests = 1
    # }
  
  }
  ingress {
    external_enabled = true
    target_port = 80
    traffic_weight {
      percentage = 100
    }
  }
 
}

resource "time_sleep" "wait_60_seconds" {
      create_duration = "60s"
}
    
resource "azapi_update_resource" "update_app" {
  type        = "Microsoft.App/containerApps@2022-10-01"
  resource_id = azurerm_container_app.app_http_scale.id
  
  body = jsonencode({
    properties = {
      template = {
        scale = {
          rules = [
            {
             name ="http-rule",
             http  = {
               metadata = {
                concurrentRequests = "100"
              }
             }
            }
          ]
        }
      }
    }
  })
  lifecycle {
    replace_triggered_by = [
      azurerm_container_app.app_http_scale
    ]
  }
  depends_on = [
    time_sleep.wait_60_seconds
  ]
}