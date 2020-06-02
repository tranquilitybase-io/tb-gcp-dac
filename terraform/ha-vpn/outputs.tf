output "ha_vpn_gw" {
  description = "HA VPN Gateway Name"
  value       = var.ha_vpn_gateway
}

output "peer_gw" {
  description = "Peer Gateway Name"
  value       = var.peer_gw_name
}

output "peer_gw_ip_0" {
  description = "First Peer Gateway External IP address"
  value       = var.peer_gw_int_0
}

output "peer_gw_ip_1" {
  description = "Second Peer Gateway External IP address"
  value       = var.peer_gw_int_1
}

output "tunnel_name_0" {
  description = "First VPN tunnel name"
  value       = var.tunnel_name_if0
}

output "tunnel_name_1" {
  description = "Second VPN tunnel name"
  value       = var.tunnel_name_if1
}

output "cloud_router_name" {
  description = "Cloud Router Name"
  value       = var.cloud_router
}