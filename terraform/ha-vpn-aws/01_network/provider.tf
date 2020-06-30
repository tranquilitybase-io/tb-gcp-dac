provider "google" {
 version     = "~> 3.24"
 project     = var.gcp_project_id
 region      = var.gcp_region1
}

provider "google-beta" {
 version     = "~> 3.24"
 project     = var.gcp_project_id
 region      = var.gcp_region1
}
