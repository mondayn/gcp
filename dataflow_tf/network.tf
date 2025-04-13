resource "google_compute_network" "my_network" {
  name                    = "my-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "my_subnet" {
  name                     = "my-subnet"
  ip_cidr_range            = "10.0.1.0/24"
  network                  = google_compute_network.my_network.id
  region                   = var.region
  private_ip_google_access = true
}

resource "google_compute_firewall" "allow_http_egress" {
  name      = "allow-http-egress"
  network   = google_compute_network.my_network.id
  direction = "EGRESS"
  allow { protocol = "icmp" }
  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }
  # target_tags = ["dataflow"]
  destination_ranges = ["0.0.0.0/0"]
}
