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

import yaml
from python_terraform import Terraform
import config
from gcpdac.utils import labellize, random_element, sanitize

logger = config.logger


def run_terraform(solutiondata, terraform_command):
    # builds and destroys solution
    # The configuration YAML file read by read_config_map() determines where this new infrastructure should sit
    # within a GCP project, as well as setting other properties like billing.
    # Accepts JSON content-type input.
    # returns return code and repsonse from terraform
    tf_data = solutiondata
    solution_id = solutiondata.get("id")
    logger.debug("solution_id is %s", solution_id)
    solution_name = solutiondata.get("name", "NoneAsDelete")

    labellizedCostCentre = labellize(solutiondata.get("costCentre", "NoneAsDelete"))
    tf_data['cost_centre'] = labellizedCostCentre
    labellizedBusinessUnit = labellize(solutiondata.get("businessUnit", "NoneAsDelete"))
    tf_data['business_unit'] = labellizedBusinessUnit
    envs: list = solutiondata.get("environments", list())
    tf_data['environments'] = [sanitize(x) for x in envs]
    # TODO return the labellized versions
    config = read_config_map()

    region = config['region']
    tf_data['region'] = region
    tf_data['activator_folder_id'] = config['activator_folder_id']
    tf_data['billing_account'] = config['billing_account']
    tf_data['shared_vpc_host_project'] = config['shared_vpc_host_project']
    tf_data['shared_network_name'] = config['shared_network_name']
    tf_data['shared_networking_id'] = config['shared_networking_id']
    tf_data['root_id'] = config['activator_folder_id']
    tb_discriminator = config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator
    # added to ensure all resources can be deleted and recreated
    tf_data['random_element'] = random_element(num_chars=6)

    backend_prefix = str(solution_id) + '-' + tb_discriminator
    tf_data['solution_name'] = solution_name

    # TODO generate tfvars file from input - currently only region_zone in this file
    env_data = '/app/terraform/input.tfvars'
    # TODO pass region_zone in
    region_zone = region + "-b"
    tf_data['region_zone'] = region_zone

    terraform_source_path = '/app/terraform/'  # this should be the param to python script

    # TODO create 'modules.tf' file for solution. Will have correct number of environments
    # currently using a 'hard coded' modules.tf file that creates 3 environment projects

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)
    terraform_state_bucket = config['terraform_state_bucket']

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    if terraform_command.lower() == 'apply'.lower():
        return terraform_apply(env_data, tf)
    else:
        return terraform_destroy(env_data, tf)


def terraform_init(backend_prefix, terraform_state_bucket, tf: Terraform):
    return_code, stdout, stderr = tf.init(capture_output=False,
                                          backend_config={'bucket': terraform_state_bucket,
                                                          'prefix': backend_prefix})
    logger.debug('Terraform init return code is {}'.format(return_code))
    logger.debug('Terraform init stdout is {}'.format(stdout))
    logger.debug('Terraform init stderr is {}'.format(stderr))


def terraform_apply(env_data, tf: Terraform):
    return_code, stdout, stderr = tf.apply(skip_plan=True, var_file=env_data, capture_output=True)
    logger.debug('Terraform apply return code is {}'.format(return_code))
    logger.debug('Terraform apply stdout is {}'.format(stdout))
    logger.debug("Terraform apply stderr is {}".format(stderr))
    if return_code == 0:
        tf_state = terraform_show(tf)
    else:
        tf_state = {}
    return {"tf_return_code": return_code, "tf_state": tf_state}


def terraform_show(tf: Terraform):
    return_code, tf_state, stdout = tf.show(json=True)
    logger.debug('Terraform state is {}'.format(tf_state))
    logger.debug('Terraform show return code is {}'.format(return_code))
    logger.debug('Terraform show stdout is {}'.format(stdout))
    return tf_state


def terraform_destroy(env_data, tf):
    return_code, stdout, stderr = tf.destroy(var_file=env_data, capture_output=False)
    logger.debug('Terraform destroy return code is {}'.format(return_code))
    logger.debug('Terraform destroy stdout is {}'.format(stdout))
    logger.debug('Terraform destroy stderr is {}'.format(stderr))
    return {"tf_return_code": return_code}


def read_config_map():
    # Returns the EC configuration as a dictionary
    try:
        with open("/app/ec-config.yaml", 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.exception("Failed to parse EC YAML after successfully opening - {}".format(exc))
                raise
    except Exception:
        logger.exception("Failed to load EC YAML file")
        raise
