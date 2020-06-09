output "ha_vpn_gw" {
  description = "HA VPN Gateway Name"
  value       = var.ha_vpn_gateway
}


output "cloud_router_name" {
  description = "Cloud Router Name"
  value       = var.cloud_router
}

output "gcp_asn" {
  description = "GCP asn"
  value       = var.gcp_asn
}