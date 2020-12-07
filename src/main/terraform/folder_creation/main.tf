# Copyright 2019 The Tranquility Base Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###
# Root module (activates other modules)
###

provider "google" {
  region = var.region
  zone   = var.region_zone
  version = "~> 3.17"
}

//provider "google-beta" {
//  alias   = "shared-vpc"
//  region  = var.region
//  zone    = var.region_zone
//  project = module.shared_projects.shared_networking_id
//  version = "~> 3.17"
//}
//
terraform {
  backend "gcs" {
    # The bucket name below is overloaded at every run with
    # `-backend-config="bucket=${terraform_state_bucket_name}"` parameter
    # templated into the `bootstrap.sh` script
    bucket = "terraformdevstate"
  }
}

//module "apis_activation" {
//  source = "../../apis-activation"
//
//  ec_project_id          = module.shared_projects.shared_ec_id
//  bastion_project_id              = module.shared_projects.shared_bastion_id
//  host_project_id         = module.shared_projects.shared_networking_id
//  service_projects_number = var.service_projects_number
//  service_project_ids     = [module.shared_projects.shared_secrets_id, module.shared_projects.shared_itsm_id, module.shared_projects.shared_ec_id]
//}

