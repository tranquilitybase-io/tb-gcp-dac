# python app writes to this file to determine what modules get executed and how many times

# example follows - this would be written by python app before terraform executed
module "solution_folder" {
  source = "../tbase_folder"
  region = var.region
  region_zone = var.region_zone
  root_id = var.root_id
  folder_name = var.solution_name
  tb_discriminator = var.tb_discriminator
}
