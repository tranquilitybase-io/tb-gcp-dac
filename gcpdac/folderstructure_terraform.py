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
from python_terraform import Terraform

import config
from gcpdac.terraform_utils import terraform_init, terraform_apply, terraform_destroy

logger = config.logger

def run_terraform(folderstructuredata, terraform_command):
    # builds and destroys a folder structure
    # The configuration YAML file read by read_config_map() determines where this new infrastructure should sit
    # within a GCP project, as well as setting other properties like billing.
    # Accepts JSON content-type input.
    # returns return code and response from terraform
    tf_data = dict()
    folderStructure = folderstructuredata.get("folderStructure")

    ec_config = config.read_config_map()

    # TODO implement

    ec_config = config.read_config_map()

    region = ec_config['region']
    tf_data['region'] = region
    tf_data['billing_account'] = ec_config['billing_account']
    tf_data['shared_vpc_host_project'] = ec_config['shared_vpc_host_project']
    tf_data['shared_network_name'] = ec_config['shared_network_name']
    tf_data['shared_networking_id'] = ec_config['shared_networking_id']
    tf_data['root_id'] = ec_config['activator_folder_id']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator
    # added to ensure all resources can be deleted and recreated

    backend_prefix = 'folders-' + tb_discriminator

    # TODO generate tfvars file from input - cu rrently only region_zone in this file
    env_data = '/app/terraform/input.tfvars'
    # TODO pass region_zone in
    region_zone = region + "-b"
    tf_data['region_zone'] = region_zone

    terraform_source_path = '/app/terraform/folder_structure_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)
    terraform_state_bucket = ec_config['terraform_state_bucket']

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    if terraform_command.lower() == 'apply'.lower():
        return terraform_apply(env_data, tf)
    else:
        return terraform_destroy(env_data, tf)
