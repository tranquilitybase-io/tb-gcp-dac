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
gcp_credentials_file_path = "../../credentials.json"
gcp_project_id = "bootstrap-29658c9f"
gcp_region1 = "us-west1"
gcp_region2 = "us-east1"
network1 = "network-a"
network1_subnet1 = "subnet-us-west1"
network1_subnet2 = "subnet-us-east1"
subnet1_ip_cidr = "10.0.1.0/24"
subnet2_ip_cidr = "10.0.2.0/24"
ha_vpn_gateway = "ha-vpn-gw-tranquilitybase"
cloud_router = "tranquilitybase-router-tranquilitybase"
gcp_asn = "65001"
peer_asn = "65002"
peer_gw_name = "tranquilitybase-peer-gw"
peer_gw_int_0 = "209.119.81.228"
peer_gw_int_1 = "209.119.82.228"
tunnel_name_if0 = "tunnel-a-to-on-prem-if-0"
shared_secret = "TODO"
tunnel_name_if1 = "tunnel-a-to-on-prem-if-1"
router_int0 = "if-tunnel-a-to-on-prem-if-0"
router_int1 = "if-tunnel-a-to-on-prem-if-1"
router_int_name_0 = "bgp-peer-tunnel-a-to-on-prem-if-0"
router_int_name_1 = "bgp-peer-tunnel-a-to-on-prem-if-1"
bgp_peer_0 = "bgp-peer-tranquilitybase-0"
bgp_peer_1 = "bgp-peer-tranquilitybase-1"
on-prem-bgp-ip-0 = "169.254.0.2"
on-prem-bgp-ip-1 = "169.254.0.5"
google-bgp-ip-0 = "169.254.0.1/30"
google-bgp-ip-1 = "169.254.0.6/30"




