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
from python_terraform import Terraform

import config
from gcpdac.exceptions import DacError
from gcpdac.shell_utils import delete_repo
from gcpdac.terraform_utils import terraform_apply, terraform_destroy, terraform_init
from gcpdac.utils import labellize, random_element, sanitize

logger = config.logger


def create_solution(solutiondata):
    logger.debug("solution_id is %s", type(solutiondata))

    ec_config = config.read_config_map()
    terraform_source_path = '/app/terraform/solution_creation'
    terraform_state_bucket = ec_config['terraform_state_bucket']
    terraform_backend_prefix = get_solution_backend_prefix(solutiondata.get("id"), ec_config['tb_discriminator'])

    tf_data = dict()
    try:
        solution_id = solutiondata['id']
        logger.debug("solution_id is %s", solution_id)
        tf_data['solution_id'] = solution_id
        tf_data['cost_centre'] = labellize(solutiondata['costCentre'])
        tf_data['business_unit'] = labellize(solutiondata['businessUnit'])
        tf_data['deployment_folder_id'] = solutiondata['deploymentFolderId']
        tf_data['environments'] = [sanitize(x) for x in (solutiondata.get('environments', list()))]

        tf_data['solution_name'] = solutiondata["name"]
        team: dict = solutiondata['team']

        tf_data['team'] = labellize(team['name'])
        team_members: dict = dict()
        for team_member in team['teamMembers']:
            member_email = team_member['user']['email']
            cloud_identity_group = team_member['role']['cloudIdentityGroup']
            team_members[member_email] = cloud_identity_group

        logger.debug("tf_data {}".format(team_members))

        tf_data['team_members'] = team_members
        region = ec_config['region']
        tf_data['region'] = region
        tf_data['billing_account'] = ec_config['billing_account']
        tf_data['shared_vpc_host_project'] = ec_config['shared_vpc_host_project']
        tf_data['shared_network_name'] = ec_config['shared_network_name']
        tf_data['shared_networking_id'] = ec_config['shared_networking_id']
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

    return response


def delete_solution(solutiondata):
    tf_data = dict()
    solution_id = solutiondata.get("id")
    logger.debug("solution_id is %s", solution_id)

    tf_data['cost_centre'] = None
    tf_data['business_unit'] = None
    tf_data['deployment_folder_id'] = None
    tf_data['environments'] = list()
    tf_data['solution_name'] = None
    tf_data['solution_id'] = None
    tf_data['random_element'] = None
    tf_data['region'] = None
    tf_data['region_zone'] = None
    tf_data['tb_discriminator'] = None
    tf_data['team'] = None

    ec_config = config.read_config_map()

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

    # delete_workspace_repo(ec_config, tf)

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
