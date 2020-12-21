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
import json
import traceback

from src.main.python.tranquilitybase.gcpdac.configuration.eaglehelper import EagleConfigHelper
from src.main.python.tranquilitybase.gcpdac.core.exceptions.exceptions import DacError
from src.main.python.tranquilitybase.gcpdac.core.shell_wrappers.shell_utils import add_access_to_folders, delete_repo
from src.main.python.tranquilitybase.gcpdac.core.terraform.terraform_utils import *
from src.main.python.tranquilitybase.lib.common.utils import *

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))


def create_solution(solutiondata):
    ec_config = EagleConfigHelper.config_dict
    terraform_source_path = '/app/terraform/solution_creation'
    terraform_state_bucket = ec_config['terraform_state_bucket']
    terraform_backend_prefix = get_solution_backend_prefix(solutiondata.get("id"), ec_config['tb_discriminator'])

    tf_data = dict()
    try:
        solution_id = solutiondata['id']
        logger.debug("solution_id is %s", solution_id)
        tf_data['solution_id'] = solution_id
        tf_data['cost_code'] = labellize(solutiondata['costCentre'])
        tf_data['business_unit'] = labellize(solutiondata['businessUnit'])
        deployment_folder_id = solutiondata['deploymentFolderId']
        tf_data['deployment_folder_id'] = deployment_folder_id
        tf_data['created_by'] = labellize(solutiondata.get('createdBy', 'labeltba'))
        environments = solutiondata.get("environments", list())
        for environment in environments:
            environment['name'] = sanitize(environment['name'])
            environment['shared_vpc_host_project'] = environment['sharedVPCProjectId']

        tf_data['environments'] = environments

        tf_data['solution_name'] = solutiondata["name"]
        team: dict = solutiondata['team']

        tf_data['team'] = labellize(team['name'])
        team_members = list()
        for team_member in team['teamMembers']:
            member_email = team_member['user']['email']
            team_members.append("user:{}".format(member_email))

        tf_data['team_members'] = [x for x in team_members]

        region = ec_config['region']
        tf_data['region'] = region
        tf_data['billing_account'] = ec_config['billing_account']
        shared_vpc_host_project = ec_config['shared_vpc_host_project']
        if shared_vpc_host_project != None:
            tf_data['shared_vpc_host_project'] = shared_vpc_host_project
        else:
            logger.info("Shared VPC Host Project not supplied - network will not be overridden")
        tb_discriminator = ec_config['tb_discriminator']
        tf_data['tb_discriminator'] = tb_discriminator
        # added to ensure all resources can be deleted and recreated
        tf_data['random_element'] = random_element(num_chars=6)
        # TODO pass region_zone in - comes from UI?
        tf_data['region_zone'] = region + "-b"
        logger.debug("tf_data {}".format(tf_data))
    except Exception as ex:
        logger.debug(traceback.format_exc())
        traceback.format_exc()
        raise DacError(ex, "Error occurred in deploy solution")

    # Call terraform
    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(terraform_backend_prefix, terraform_state_bucket, tf)

    response = terraform_apply(None, tf)
    logger.debug("response {}".format(response))

    add_access_to_folders(bottom_level_folder_id=deployment_folder_id, users=team_members, top_level_folder_id=ec_config["activator_folder_id"])

    return response


def delete_solution(solutiondata):
    tf_data = dict()
    solution_id = solutiondata.get("id")
    logger.debug("solution_id is %s", solution_id)

    tf_data['cost_code'] = None
    tf_data['business_unit'] = None
    tf_data['deployment_folder_id'] = None
    tf_data['environments'] = list()
    tf_data['solution_name'] = None
    tf_data['solution_id'] = None
    tf_data['random_element'] = None
    tf_data['region'] = None
    tf_data['region_zone'] = None
    tf_data['tb_discriminator'] = None
    tf_data['created_by'] = None
    tf_data['team'] = None
    # tf_data['shared_vpc_host_project'] = None
    tf_data['team_members'] = list()

    ec_config = EagleConfigHelper.config_dict

    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    env_data = None

    terraform_state_bucket = ec_config['terraform_state_bucket']
    # location of this solution's state with terraform bucket
    backend_prefix = get_solution_backend_prefix(solution_id, tb_discriminator)
    # source of the terraform used for this deployment
    terraform_source_path = '/app/terraform/solution_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)


def delete_workspace_repo(ec_config, tf):
    _, tf_state_json, _ = tf.show(json=True)
    tf_state: dict = json.loads(tf_state_json)
    if 'values' in tf_state:
        # only remove if state exists
        solution_name = tf_state['values']['outputs']['solution_folder']['value']['display_name']
        logger.debug("solution_name {}".format(solution_name))
        repo_name = "{}_workspace".format(solution_name)
        workspace_project_id = tf_state['values']['outputs']['workspace_project']['value']['project_id']
        logger.debug("workspace_project_id {}".format(workspace_project_id))
        eagle_project_id = ec_config['ec_project_name']
        logger.debug("eagle_project_id {}".format(eagle_project_id))
        delete_repo(repo_name, workspace_project_id, eagle_project_id)


def get_solution_backend_prefix(solution_id, tb_discriminator):
    return 'solution-' + str(solution_id) + '-' + tb_discriminator
