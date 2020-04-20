# python app writes to this file to determine what modules get executed and how many times


# example follows - this would be written by python app before terraform executed
module "solution_folder" {
  source = "./solution_folder"
  region = var.region
  region_zone = var.region_zone
  root_id = var.root_id
  solution_name = "test_solution"
}

module "dev_environment" {
  source = "./environment_project"
  project_name = "dev-env"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.solution_id
  tb_discriminator = "abcde"
}

module "staging_environment" {
  source = "./environment_project"
  project_name = "staging-env"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.solution_id
  tb_discriminator = "abcde"
}

module "prod_environment" {
  source = "./environment_project"
  project_name = "prod-env"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.solution_id
  tb_discriminator = "abcde"
}