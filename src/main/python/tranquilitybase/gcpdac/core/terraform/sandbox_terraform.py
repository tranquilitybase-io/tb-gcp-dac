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
# --- Logger ---
import inspect

from src.main.python.tranquilitybase.gcpdac.core.terraform.terraform_config import get_terraform_root
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))

import traceback
from src.main.python.tranquilitybase.gcpdac.core.exceptions.exceptions import DacError
from src.main.python.tranquilitybase.gcpdac.core.terraform.terraform_utils import *
from src.main.python.tranquilitybase.lib.common.utils import random_element, folderize, labellize
from src.main.python.tranquilitybase.gcpdac.configuration.eaglehelper import EagleConfigHelper


def create_sandbox(sandboxdata):
    ec_config = EagleConfigHelper.config_dict
    terraform_source_path = get_terraform_root() + 'sandbox_creation'
    terraform_state_bucket = ec_config['terraform_state_bucket']
    terraform_backend_prefix = get_sandbox_backend_prefix(sandboxdata.get("id"), ec_config['tb_discriminator'])

    tf_data = dict()
    try:
        sandbox_id = sandboxdata['id']
        logger.debug("sandbox_id is %s", sandbox_id)
        random_string = random_element(num_chars=6)
        tf_data['sandbox_id'] = sandbox_id
        deployment_folder_id = sandboxdata['deploymentFolderId']
        tf_data['deployment_folder_id'] = deployment_folder_id

        tf_data['sandbox_name'] = "{}-{}".format(sandboxdata["name"], random_string)  # TODO rename
        tf_data['sandbox_folder_name'] = "{}-{}".format(folderize(sandboxdata["name"]), random_string)  # TODO rename

        region = ec_config['region']
        tf_data['region'] = region
        tf_data['billing_account'] = ec_config['billing_account']
        tb_discriminator = ec_config['tb_discriminator']
        tf_data['tb_discriminator'] = tb_discriminator
        # added to ensure all resources can be deleted and recreated
        # TODO pass region_zone in - comes from UI?
        tf_data['region_zone'] = region + "-b"
        logger.debug("tf_data {}".format(tf_data))

        tf_data['sandbox_project_id'] = "sandbox-{}-{}".format(random_element(num_chars=6), tb_discriminator)

        iam_accounts = list()
        team_cloud_identity_group = sandboxdata.get('teamCloudIdentityGroup', None)
        if team_cloud_identity_group != None:
            iam_accounts.append("group:{}".format(team_cloud_identity_group))
        tf_data["iam_accounts"] = iam_accounts

        labels = dict()
        labels['environment'] = "sandbox"
        labels['team'] = labellize(sandboxdata['teamName'])
        labels['created-by'] = labellize(sandboxdata.get('createdBy', 'labeltba'))
        labels['cost-code'] = labellize(sandboxdata['costCode'])
        labels['business-unit'] = labellize(sandboxdata['businessUnit'])
        labels['sandbox-id'] = sandbox_id
        tf_data['labels'] = labels

    except Exception as ex:
        logger.debug(traceback.format_exc())
        traceback.format_exc()
        raise DacError(ex, "Error occurred in deploy sandbox")

    # Call terraform
    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(terraform_backend_prefix, terraform_state_bucket, tf)

    response = terraform_apply(None, tf)
    logger.debug("response {}".format(response))

    return response


def delete_sandbox(sandboxdata):
    tf_data = dict()
    sandbox_id = sandboxdata.get("id")
    logger.debug("sandbox_id is %s", sandbox_id)

    tf_data['deployment_folder_id'] = None
    tf_data['sandbox_name'] = None
    tf_data['sandbox_folder_name'] = None
    tf_data['sandbox_id'] = None
    tf_data['sandbox_project_id'] = None
    tf_data['random_element'] = None
    tf_data['region'] = None
    tf_data['region_zone'] = None
    tf_data['labels'] = None
    tf_data['iam_accounts'] = None

    ec_config = EagleConfigHelper.config_dict

    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    env_data = None

    terraform_state_bucket = ec_config['terraform_state_bucket']
    # location of this sandbox's state with terraform bucket
    backend_prefix = get_sandbox_backend_prefix(sandbox_id, tb_discriminator)
    # source of the terraform used for this deployment
    terraform_source_path = get_terraform_root() + 'sandbox_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)


def get_sandbox_backend_prefix(sandbox_id, tb_discriminator):
    return 'sandbox-' + str(sandbox_id) + '-' + tb_discriminator
