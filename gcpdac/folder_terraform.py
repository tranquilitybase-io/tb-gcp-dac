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


def create_folder(folderDetails):
    # builds and destroys a folder
    # The configuration YAML file read by read_config_map() determines where this new infrastructure should sit
    # within a GCP project, as well as setting other properties like billing.
    # Accepts JSON content-type input.
    # returns return code and response from terraform
    tf_data = dict()
    logger.debug("folder is %s", folderDetails)
    folder = folderDetails.get('folder')

    folder_name = folder['folderName']
    tf_data['folder_name'] = folder_name
    tf_data['parent_folder_id'] = folder['parentFolderId']

    ec_config = config.read_config_map()

    region = ec_config['region']
    tf_data['region'] = region
    # TODO pass region_zone in
    region_zone = region + "-b"
    tf_data['region_zone'] = region_zone
    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    terraform_state_bucket = ec_config['terraform_state_bucket']
    tf_data['tb_discriminator'] = tb_discriminator

    backend_prefix = folder_name + '-' + tb_discriminator

    # TODO generate tfvars file from input - currently only region_zone in this file
    env_data = '/app/terraform/input.tfvars'

    terraform_source_path = '/app/terraform/folder_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_apply(env_data, tf)

def delete_folder(folder):
    tf_data = dict()
    folder_name = folder.get("id")
    tf_data['folder_name'] = folder_name
    tf_data['parent_folder_id'] = '0'  # set but not used on destroy

    ec_config = config.read_config_map()
    region = ec_config['region']
    tf_data['region'] = region
    # TODO pass region_zone in
    region_zone = region + "-b"
    tf_data['region_zone'] = region_zone
    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator
    terraform_state_bucket = ec_config['terraform_state_bucket']

    env_data = '/app/terraform/input.tfvars'
    backend_prefix = folder_name + '-' + tb_discriminator
    terraform_source_path = '/app/terraform/folder_creation'
    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)
    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)
