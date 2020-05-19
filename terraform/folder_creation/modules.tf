module "tbase_folder" {
  source = "../tbase_folder"
  region = var.region
  region_zone = var.region_zone
  tb_discriminator = var.tb_discriminator
  folder_name = var.folder_name
  parent_folder_id = var.parent_folder_id
}
