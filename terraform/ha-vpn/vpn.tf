
resource "google_compute_network" "ha-vpn-test-network" {
  name                    = var.network1
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
  description = "Back up VPN connection between GCP US and Cisco 5505 on prem"
}

resource "google_compute_subnetwork" "network1-subnet1" {
  name   = var.network1_subnet1
  ip_cidr_range = var.subnet1_ip_cidr
  region = var.gcp_region1
  network  = var.network1
  depends_on = [google_compute_network.ha-vpn-test-network]
}

resource "google_compute_subnetwork" "network1-subnet2" {
  name   = var.network1_subnet2
  ip_cidr_range = var.subnet2_ip_cidr
  region = var.gcp_region2
  network  = var.network1
  depends_on = [google_compute_network.ha-vpn-test-network]
}

// Create HA VPN gateway
resource "google_compute_ha_vpn_gateway" "ha_gateway1" {
  provider = "google-beta"
  region = var.gcp_region1
  name     = var.ha_vpn_gateway
  network  = var.network1
  depends_on = [google_compute_network.ha-vpn-test-network]
}

// Create cloud router
resource "google_compute_router" "router-a" {
  name    = var.cloud_router
  network  = var.network1
  bgp {
    asn = var.gcp_asn
    advertise_mode    = "CUSTOM"
    advertised_groups = ["ALL_SUBNETS"]
    advertised_ip_ranges {
      range = google_compute_subnetwork.network1-subnet1.ip_cidr_range
    }
    advertised_ip_ranges {
      range = google_compute_subnetwork.network1-subnet2.ip_cidr_range
    }
    
  }
  depends_on = [google_compute_network.ha-vpn-test-network]
}

// Create external aka peer gateway
resource "google_compute_external_vpn_gateway" "external_gateway" {
  provider        = "google-beta"
  name            = var.peer_gw_name
  redundancy_type = "TWO_IPS_REDUNDANCY"
  description     = "An externally managed VPN gateway"
  interface {
    id = 0
    ip_address = var.peer_gw_int_0
  }
  interface {
    id = 1
    ip_address = var.peer_gw_int_1
  }
}

// Create first VPN tunnel
resource "google_compute_vpn_tunnel" "tunnel0" {
  provider         = "google-beta"
  name             = var.tunnel_name_if0
  region           = var.gcp_region1
  vpn_gateway      = var.ha_vpn_gateway
  peer_external_gateway = var.peer_gw_name
  peer_external_gateway_interface = 0
  shared_secret    = var.shared_secret
  router           = var.cloud_router
  vpn_gateway_interface = 0
  depends_on = [google_compute_router.router-a,google_compute_ha_vpn_gateway.ha_gateway1,google_compute_external_vpn_gateway.external_gateway]
}

// Create second VPN tunnel
resource "google_compute_vpn_tunnel" "tunnel1" {
  provider         = "google-beta"
  name             = var.tunnel_name_if1
  region           = var.gcp_region1
  vpn_gateway      = var.ha_vpn_gateway
  peer_external_gateway = var.peer_gw_name
  peer_external_gateway_interface = 1
  shared_secret    = var.shared_secret
  router           = var.cloud_router
  vpn_gateway_interface = 1
  depends_on = [google_compute_router.router-a,google_compute_ha_vpn_gateway.ha_gateway1,google_compute_external_vpn_gateway.external_gateway]
}

// Create first cloud router interface
resource "google_compute_router_interface" "router1_interface0" {
  provider         = "google-beta"
  name       = var.router_int0
  router     = var.cloud_router
  region     = var.gcp_region1
  ip_range   = var.google-bgp-ip-0
  vpn_tunnel = var.tunnel_name_if0
  depends_on = [google_compute_router.router-a,google_compute_vpn_tunnel.tunnel0]

}

// Create first BGP peer
resource "google_compute_router_peer" "router1_peer0" {
  provider         = "google-beta"
  name                      = var.bgp_peer_0
  router                    = var.cloud_router
  region                    = var.gcp_region1
  peer_asn                  = var.peer_asn
  advertised_route_priority = 100
  interface                 = var.router_int0
  depends_on = [google_compute_router.router-a,google_compute_router_interface.router1_interface0]
  peer_ip_address = var.on-prem-bgp-ip-0

}

// Create second cloud router interface
resource "google_compute_router_interface" "router1_interface1" {
  provider         = "google-beta"
  name       = var.router_int1
  router     = var.cloud_router
  region     = var.gcp_region1
  ip_range   = var.google-bgp-ip-1
  vpn_tunnel = var.tunnel_name_if1
  depends_on = [google_compute_router.router-a,google_compute_vpn_tunnel.tunnel1]
}

// Create second BGP peer
resource "google_compute_router_peer" "router1_peer1" {
  provider         = "google-beta"
  name                      = var.bgp_peer_1
  router                    = var.cloud_router
  region                    = var.gcp_region1
  peer_asn                  = var.peer_asn
  advertised_route_priority = 100
  interface                 = var.router_int1
  depends_on = [google_compute_router.router-a,google_compute_router_interface.router1_interface1]
  peer_ip_address = var.on-prem-bgp-ip-1
}
