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

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))

from src.main.python.tranquilitybase.gcpdac.configuration.eaglehelper import EagleConfigHelper
from src.main.python.tranquilitybase.gcpdac.core.terraform.terraform_utils import terraform_init, terraform_apply, \
    terraform_destroy


def create_folder(folderDetails):
    # builds and destroys a folder
    # The configuration YAML file read by read_config_map() determines where this new infrastructure should sit
    # within a GCP project, as well as setting other properties like billing.
    # Accepts JSON content-type input.
    # returns return code and response from terraform
    tf_data = dict()
    ec_config = EagleConfigHelper.config_dict
    logger.debug("folder is %s", folderDetails)
    folder = folderDetails.get('folder')

    folder_name = folder['folderName']
    tf_data['folder_name'] = folder_name
    tf_data['parent_folder_id'] = folder['parentFolderId']

    region = ec_config['region']
    tf_data['region'] = region
    # TODO pass region_zone in - from UI?
    tf_data['region_zone'] = region + "-b"
    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    # env_data = '/app/terraform/input.tfvars'
    env_data = None
    backend_prefix = get_folder_backend_prefix(folder_name, tb_discriminator)
    terraform_state_bucket = ec_config['terraform_state_bucket']
    terraform_source_path = '/app/terraform/folder_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_apply(env_data, tf)


def delete_folder(folder):
    tf_data = dict()
    folder_name = folder.get("id")

    # variables not used on delete
    tf_data['parent_folder_id'] = None
    tf_data['random_element'] = None
    tf_data['region'] = None
    tf_data['region_zone'] = None
    tf_data['tb_discriminator'] = None
    tf_data['folder_name'] = None

    ec_config = EagleConfigHelper.config_dict
    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    env_data = None

    backend_prefix = get_folder_backend_prefix(folder_name, tb_discriminator)
    terraform_state_bucket = ec_config['terraform_state_bucket']
    terraform_source_path = '/app/terraform/folder_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)
    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)


def get_folder_backend_prefix(folder_name, tb_discriminator):
    return 'folder-' + folder_name + '-' + tb_discriminator
