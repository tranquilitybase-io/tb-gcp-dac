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
  cost_centre = var.cost_centre
  random_element = var.random_element
  billing_account = var.billing_account
  solution_name = var.solution_name
  solution_id = var.solution_id
  team = var.team
  member_role = var.member_role
  team_members = var.team_members
}


module "environment_projects" {
  source = "../environment_project"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.folder_id
  tb_discriminator = var.tb_discriminator
  business_unit = var.business_unit
  cost_centre = var.cost_centre
  random_element = var.random_element
  billing_account = var.billing_account
  environments = var.environments
  solution_name = var.solution_name
  solution_id = var.solution_id
  team = var.team
  member_role = var.member_role
  team_members = var.team_members

}

