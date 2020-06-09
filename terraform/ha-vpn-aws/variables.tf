variable gcp_credentials_file_path {
  type = "string"
  default = "zain-sandbox-ec1ddc14dd8e.json"
}

variable "gcp_project_id" {
  description = "Enter GCP Project ID."
  type = "string"
  default = "zain-sandbox"
}

variable gcp_region1 {
  default = "us-west1"
}

variable gcp_region2 {
  default = "us-east1"
}

variable network1 {
  default = "network-a"
}

variable network1_subnet1 {
  default = "subnet-us-west1"
}

variable network1_subnet2 {
  default = "subnet-us-east1"
}

variable subnet1_ip_cidr {
  default = "10.0.1.0/24"
}

variable subnet2_ip_cidr {
  default = "10.0.2.0/24"
}

variable ha_vpn_gateway {
  default = "ha-vpn-gw-tranquilitybase"
}

variable cloud_router {
  default = "tranquilitybase-router-tranquilitybase"
}

variable gcp_asn {
  default = "65001"
}

variable gw1_tunnel1_asn {
  default = "65002"
}

variable gw1_tunnel2_asn {
  default = "65002"
}

variable gw2_tunnel1_asn {
  default = "65002"
}

variable gw2_tunnel2_asn {
  default = "65002"
}

variable peer_gw_name {
  default = "aws-gateway"
}

variable aws_gw1_tunnel1_address {
  type = "string"
  default = "209.119.81.228"
}

variable aws_gw1_tunnel2_address {
  type = "string"
  default = "209.119.82.228"
}

variable aws_gw2_tunnel1_address {
  type = "string"
  default = "209.119.81.228"
}

variable aws_gw2_tunnel2_address {
  type = "string"
  default = "209.119.82.228"
}

variable aws_gw1_tunnel1_shared_secret {
  type = "string"
}

variable aws_gw1_tunnel2_shared_secret {
  type = "string"
}

variable aws_gw2_tunnel1_shared_secret {
  type = "string"
}

variable aws_gw2_tunnel2_shared_secret {
  type = "string"
}

variable tunnel_name_if0 {
  default = "tunnel-1-to-aws"
}

variable tunnel_name_if1 {
  default = "tunnel-2-to-aws"
}

variable tunnel_name_if2 {
  default = "tunnel-3-to-aws"
}

variable tunnel_name_if3 {
  default = "tunnel-4-to-aws"
}

variable router_int0 {
  default = "tunnel-1-to-aws-if-0"
}

variable router_int1 {
  default = "tunnel-2-to-aws-if-0"
}

variable router_int2 {
  default = "tunnel-1-to-aws-if-1"
}

variable router_int3 {
  default = "tunnel-2-to-aws-if-1"
}

variable router_int_name_0 {
  default = "bgp-peer-tunnel-a-to-on-prem-if-0"
}

variable router_int_name_1 {
  default = "bgp-peer-tunnel-a-to-on-prem-if-1"
}

variable bgp_peer_0 {
  default = "peer-0"
}

variable bgp_peer_1 {
  default = "peer-1"
}

variable bgp_peer_2 {
  default = "peer-2"
}

variable bgp_peer_3 {
  default = "peer-3"
}

variable aws_gw1_tunnel1_inside_address {
  type = "string"
  default = "169.254.0.6"
}

variable aws_gw1_tunnel2_inside_address {
  type = "string"
  default = "169.254.0.1"
}

variable aws_gw2_tunnel1_inside_address {
  type = "string"
  default = "169.254.0.6"
}

variable aws_gw2_tunnel2_inside_address {
  type = "string"
  default = "169.254.0.1"
}

variable aws_gw1_tunnel1_peer_ip {
  type = "string"
  default = "169.254.0.6"
}

variable aws_gw1_tunnel2_peer_ip {
  type = "string"
  default = "169.254.0.1"
}

variable aws_gw2_tunnel1_peer_ip {
  type = "string"
  default = "169.254.0.6"
}

variable aws_gw2_tunnel2_peer_ip {
  type = "string"
  default = "169.254.0.1"
}

