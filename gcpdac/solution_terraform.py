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
from gcpdac.shell_utils import create_repo
from gcpdac.terraform_utils import terraform_apply, terraform_destroy, terraform_init, NOT_USED_ON_DESTROY
from gcpdac.utils import labellize, random_element, sanitize

logger = config.logger


def create_solution(solutiondata):
    tf_data = dict()
    ec_config = config.read_config_map()

    solution_id = solutiondata.get("id")
    logger.debug("solution_id is %s", solution_id)
    tf_data['cost_centre'] = labellize(solutiondata.get("costCentre"))
    tf_data['business_unit'] = labellize(solutiondata.get("businessUnit"))
    tf_data['deployment_folder_id'] = solutiondata.get("deploymentFolderId")
    tf_data['environments'] = [sanitize(x) for x in (solutiondata.get("environments", list()))]
    tf_data['solution_name'] = solutiondata.get("name")

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

    backend_prefix = get_solution_backend_prefix(solution_id, tb_discriminator)

    # TODO remove dependency on this
    env_data = '/app/terraform/input.tfvars'
    # TODO pass region_zone in - comes from UI?
    tf_data['region_zone'] = region + "-b"

    terraform_source_path = '/app/terraform/solution_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)
    terraform_state_bucket = ec_config['terraform_state_bucket']

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    response = terraform_apply(env_data, tf)
    logger.debug("response {}".format(response))

    # Not part of terraform TODO not ideal
    workspace_project_id = response["tf_outputs"]["workspace_project"]["value"]["project_id"]
    ec_project_id = ec_config['ec_project_name']
    repo_name = "workspace_repo"
    create_repo(repo_name, workspace_project_id, ec_project_id)

    return response


def delete_solution(solutiondata):
    tf_data = dict()
    solution_id = solutiondata.get("id")
    logger.debug("solution_id is %s", solution_id)

    tf_data['cost_centre'] = NOT_USED_ON_DESTROY
    tf_data['business_unit'] = NOT_USED_ON_DESTROY
    tf_data['deployment_folder_id'] = NOT_USED_ON_DESTROY
    tf_data['environments'] = list()
    tf_data['solution_name'] = NOT_USED_ON_DESTROY
    tf_data['random_element'] = NOT_USED_ON_DESTROY
    tf_data['region'] = NOT_USED_ON_DESTROY
    tf_data['region_zone'] = NOT_USED_ON_DESTROY
    tf_data['tb_discriminator'] = NOT_USED_ON_DESTROY
    tf_data['region_zone'] = NOT_USED_ON_DESTROY

    ec_config = config.read_config_map()

    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    # TODO remove dependency on this?
    env_data = '/app/terraform/input.tfvars'

    terraform_state_bucket = ec_config['terraform_state_bucket']
    # location of this solution's state with terraform bucket
    backend_prefix = get_solution_backend_prefix(solution_id, tb_discriminator)
    # source of the terraform used for this deployment
    terraform_source_path = '/app/terraform/solution_creation'

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)


def get_solution_backend_prefix(solution_id, tb_discriminator):
    return 'solution-' + str(solution_id) + '-' + tb_discriminator
