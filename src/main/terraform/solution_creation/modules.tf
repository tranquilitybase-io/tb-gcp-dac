module "solution_folder" {
  source = "../tbase_folder"
  region = var.region
  region_zone = var.region_zone
  parent_folder_id = var.deployment_folder_id
  folder_name = var.solution_name
  tb_discriminator = var.tb_discriminator
}

module "workspace_project" {
  source = "../workspace_project"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.folder_id
  tb_discriminator = var.tb_discriminator
  business_unit = var.business_unit
  cost_code = var.cost_code
  random_element = var.random_element
  billing_account = var.billing_account
  solution_name = var.solution_name
  solution_id = var.solution_id
  team = var.team
  team_members = var.team_members
  created_by = var.created_by
  folder_access_role = var.folder_access_role
  project_access_role = var.project_access_role
  shared_vpc_host_project = var.shared_vpc_host_project
}


module "environment_projects" {
  source = "../environment_project"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.folder_id
  tb_discriminator = var.tb_discriminator
  business_unit = var.business_unit
  cost_code = var.cost_code
  random_element = var.random_element
  billing_account = var.billing_account
  environments = var.environments
  solution_name = var.solution_name
  solution_id = var.solution_id
  team = var.team
  folder_access_role = var.folder_access_role
  project_access_role = var.project_access_role
  team_members = var.team_members
  created_by = var.created_by
  shared_vpc_host_project = var.shared_vpc_host_project
}


