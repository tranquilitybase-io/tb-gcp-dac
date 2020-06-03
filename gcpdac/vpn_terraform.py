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
from gcpdac.terraform_utils import terraform_apply, terraform_destroy, terraform_init, NOT_USED_ON_DESTROY
from gcpdac.utils import labellize, random_element, sanitize

VPN_TERRAFORM_LOCATION = '/app/terraform/ha-vpn'

logger = config.logger


def create_vpn(vpndata):
    tf_data = dict()
    ec_config = config.read_config_map()

    ha_vpn_gateway = vpndata.get("ha_vpn_gateway")
    logger.debug("ha_vpn_gateway is %s", ha_vpn_gateway)

    region = ec_config['region']
    tf_data['region'] = region
    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator
    # added to ensure all resources can be deleted and recreated
    tf_data['random_element'] = random_element(num_chars=6)

    backend_prefix = get_vpn_backend_prefix(ha_vpn_gateway, tb_discriminator)

    # TODO remove dependency on this
    env_data = '/app/terraform/input.tfvars'
    # TODO pass region_zone in - comes from UI?
    tf_data['region_zone'] = region + "-b"

    terraform_source_path = VPN_TERRAFORM_LOCATION

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)
    terraform_state_bucket = ec_config['terraform_state_bucket']

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_apply(env_data, tf)


def delete_vpn(vpndata):
    tf_data = dict()
    ha_vpn_gateway = vpndata.get("ha_vpn_gateway")

    ec_config = config.read_config_map()

    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator
    backend_prefix = get_vpn_backend_prefix(ha_vpn_gateway, tb_discriminator)

    logger.debug("ha_vpn_gateway is %s", ha_vpn_gateway)

    # TODO remove dependency on this?
    env_data = '/app/terraform/input.tfvars'

    terraform_state_bucket = ec_config['terraform_state_bucket']
    # location of this solution's state with terraform bucket
    # source of the terraform used for this deployment
    terraform_source_path = VPN_TERRAFORM_LOCATION

    tf = Terraform(working_dir=terraform_source_path, variables=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)

def get_vpn_backend_prefix(ha_vpn_gateway, tb_discriminator):
    return 'vpn-' + str(ha_vpn_gateway) + '-' + tb_discriminator
