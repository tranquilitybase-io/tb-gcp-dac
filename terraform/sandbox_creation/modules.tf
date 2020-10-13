module "sandbox_folder" {
  source = "../tbase_folder"
  region = var.region
  region_zone = var.region_zone
  parent_folder_id = var.deployment_folder_id
  folder_name = var.sandbox_name
  tb_discriminator = var.tb_discriminator
}

module "sandbox_project" {
  source = "../sandbox_project"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.sandbox_folder.folder_id
  tb_discriminator = var.tb_discriminator
  billing_account = var.billing_account
  sandbox_name = var.sandbox_name
  sandbox_id = var.sandbox_id
  labels = var.labels
  iam_accounts = var.iam_accounts
  sandbox_project_id = var.sandbox_project_id
}

