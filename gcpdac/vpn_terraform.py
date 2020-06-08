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
from gcpdac.terraform_utils import terraform_apply, terraform_destroy, terraform_init, NOT_USED_ON_DESTROY, \
    terraform_plan
from gcpdac.utils import labellize, random_element, sanitize

VPN_TERRAFORM_LOCATION = '/app/terraform/ha-vpn'

logger = config.logger


def create_vpn(vpndata):
    tf_data = dict()
    ec_config = config.read_config_map()

    vpn_id = vpndata.get("id")
    logger.debug("VPN id is %s", vpn_id)

    ha_vpn_gateway = vpndata.get("ha_vpn_gateway")
    logger.debug("ha_vpn_gateway is %s", ha_vpn_gateway)

    region = ec_config['region']
    tf_data['region'] = region
    tf_data['billing_account'] = ec_config['billing_account']
    tb_discriminator = ec_config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    backend_prefix = get_vpn_backend_prefix(vpn_id, tb_discriminator)

    # set core VPN terraform s
    vpnCore = vpndata.get("vpnCore")
    # tf_data[] = vpnCore.get("bgpRoutingMode") # TODO add
    tf_data['cloud_router'] = vpnCore.get("cloudRouterName")
    # tf_data[] = vpnCore.get("description") # TODO add
    # tf_data[] = vpnCore.get("externalVpnGateway") # TODO add
    tf_data['gcp_asn'] = vpnCore.get("googleASN")
    tf_data['ha_vpn_gateway'] = vpnCore.get("haVpnGateway")
    tf_data['peer_asn'] = vpnCore.get("peerASN")
    # tf_data[] = vpnCore.get("projectName") # TODO needed?
    # tf_data[] = vpnCore.get("subnetMode") # TODO add
    # tf_data[] = vpnCore.get("vpcName") # TODO add

    # set google endpoint terraform s
    tf_data[''] = vpnCore.get("primaryGcpVpcSubnet")
    tf_data['gcp_region1'] = vpnCore.get("primaryRegion")
    tf_data[''] = vpnCore.get("primarySubnetName")
    tf_data[''] = vpnCore.get("secondaryGcpVpcSubnet")
    tf_data['gcp_region2'] = vpnCore.get("secondaryRegion")
    tf_data[''] = vpnCore.get("secondarySubnetName")

    # set remote endpoint terraform s
    tf_data[''] = vpnCore.get("primaryBgpPeer")
    tf_data[''] = vpnCore.get("primaryPeerIp")
    tf_data[''] = vpnCore.get("primaryPeerIpSubnet")
    tf_data[''] = vpnCore.get("primarySharedSecret")
    tf_data[''] = vpnCore.get("primaryVpnTunnel")
    tf_data[''] = vpnCore.get("secondaryBgpPeer")
    tf_data[''] = vpnCore.get("secondaryPeerIp")
    tf_data[''] = vpnCore.get("secondaryPeerIpSubnet")
    tf_data[''] = vpnCore.get("secondarySharedSecret")
    tf_data[''] = vpnCore.get("secondaryVpnTunnel")
    tf_data[''] = vpnCore.get("vendor")

# terraform variables
# bgp_peer_0
# bgp_peer_1
# cloud_router
# gcp_asn
# gcp_region1
# gcp_region2
# google-bgp-ip-0
# google-bgp-ip-1
# ha_vpn_gateway
# network1
# network1_subnet1
# network1_subnet2
# on-prem-bgp-ip-0
# on-prem-bgp-ip-1
# peer_asn
# peer_gw_int_0
# peer_gw_int_1
# peer_gw_name
# router_int0
# router_int1
# router_int_name_0
# router_int_name_1
# shared_secret
# subnet1_ip_cidr
# subnet2_ip_cidr
# tunnel_name_if0
# tunnel_name_if1











# TODO remove dependency on this
    env_data = None
    # TODO pass region_zone in - comes from UI?
    tf_data['region_zone'] = region + "-b"

    terraform_source_path = VPN_TERRAFORM_LOCATION

    tf = Terraform(working_dir=terraform_source_path, s=tf_data)
    tf.plan()
    terraform_state_bucket = ec_config['terraform_state_bucket']

    terraform_init(backend_prefix, terraform_state_bucket, tf)
    response = terraform_plan(env_data,tf)

    # response = terraform_apply(env_data, tf)
    return response


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

    tf = Terraform(working_dir=terraform_source_path, s=tf_data)

    terraform_init(backend_prefix, terraform_state_bucket, tf)

    return terraform_destroy(env_data, tf)


def get_vpn_backend_prefix(id, tb_discriminator):
    return 'vpn-' + str(id) + '-' + tb_discriminator
