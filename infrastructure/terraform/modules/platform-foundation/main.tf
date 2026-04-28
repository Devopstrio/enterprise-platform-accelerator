resource "azurerm_resource_group" "platform" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Platform Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "platform_k8s" {
  name                = "aks-${var.project_name}-control-plane-${var.environment}"
  location            = azurerm_resource_group.platform.location
  resource_group_name = azurerm_resource_group.platform.name
  dns_prefix          = "platform-k8s"

  default_node_pool {
    name       = "systempool"
    node_count = 3
    vm_size    = "Standard_D4s_v3"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }
}

# --- Institutional Service Catalog Metadata (Postgres) ---

resource "azurerm_postgresql_flexible_server" "platform" {
  name                   = "psql-${var.project_name}-catalog-${var.environment}"
  resource_group_name    = azurerm_resource_group.platform.name
  location               = azurerm_resource_group.platform.location
  version                = "14"
  administrator_login    = "platformadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Platform Secrets & Certificates ---

resource "azurerm_key_vault" "platform" {
  name                        = "kv-platform-${var.environment}"
  location                    = azurerm_resource_group.platform.location
  resource_group_name         = azurerm_resource_group.platform.name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}

# --- Multi-Cloud Global Artifact Hub (AWS S3) ---

resource "aws_s3_bucket" "platform_artifacts" {
  bucket = "db-enterprise-platform-artifacts-${var.environment}"
}
