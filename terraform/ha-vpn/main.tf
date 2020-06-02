provider "google" {
 version     = "~> 2.10"
 credentials = file(var.gcp_credentials_file_path)
 project     = var.gcp_project_id
 region      = var.gcp_region1
}

provider "google-beta" {
 version     = "~> 2.10"
 credentials = file(var.gcp_credentials_file_path)
 project     = var.gcp_project_id
 region      = var.gcp_region1
}

