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

variable peer_asn {
  default = "65002"
}

variable peer_gw_name {
  default = "tranquilitybase-peer-gw"
}

variable peer_gw_int_0 {
  type = "string"
  default = "209.119.81.228"
}

variable peer_gw_int_1 {
  type = "string"
  default = "209.119.82.228"
}

variable tunnel_name_if0 {
  default = "tunnel-a-to-on-prem-if-0"
}

variable shared_secret {
  type = "string"
}

variable tunnel_name_if1 {
  default = "tunnel-a-to-on-prem-if-1"
}

variable router_int0 {
  default = "if-tunnel-a-to-on-prem-if-0"
}

variable router_int1 {
  default = "if-tunnel-a-to-on-prem-if-1"
}

variable router_int_name_0 {
  default = "bgp-peer-tunnel-a-to-on-prem-if-0"
}

variable router_int_name_1 {
  default = "bgp-peer-tunnel-a-to-on-prem-if-1"
}

variable bgp_peer_0 {
  default = "bgp-peer-tranquilitybase-0"
}

variable bgp_peer_1 {
  default = "bgp-peer-tranquilitybase-1"
}

variable on-prem-bgp-ip-0 {
  type = "string"
  default = "169.254.0.2"
}

variable on-prem-bgp-ip-1 {
  type = "string"
  default = "169.254.0.5"
}

variable google-bgp-ip-0 {
  type = "string"
  default = "169.254.0.1/30"
}

variable google-bgp-ip-1 {
  type = "string"
  default = "169.254.0.6/30"
}

