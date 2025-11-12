# run build.bat to initialize or apply

#################### services
resource "google_project_service" "enable_cloudbuild" {
  project = var.project
  service = "cloudbuild.googleapis.com"
}

resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
}

resource "google_project_service" "api_gateway" {
  service = "apigateway.googleapis.com"
}

# create a bucket to store cloud function code 
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project}-fx"
  location = var.region
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "fx-src.zip"
  source = "fx-src.zip"
  bucket = google_storage_bucket.function_bucket.name
}

resource "google_cloudfunctions2_function" "summarize" {
  name     = "summarize2"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "summarize"
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    available_memory   = "256M"
    timeout_seconds    = 60
    environment_variables = {
      GCP_PROJECT = var.project
    }
  }
}

############ output ###############
output "region" {
  value = var.region
}


#################### providers.tf
provider "google" {
  project = var.project
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}


# resource "google_compute_network" "my_network" {
#   name                    = "my-network"
#   auto_create_subnetworks = false
# }

# resource "google_compute_subnetwork" "my_subnet" {
#   name                     = "my-subnet"
#   ip_cidr_range            = "10.0.1.0/24"
#   network                  = google_compute_network.my_network.id
#   region                   = "us-east4"
#   private_ip_google_access = true
# }

# resource "google_compute_firewall" "allow_http_egress" {
#   name      = "allow-http-egress"
#   network   = google_compute_network.my_network.id
#   direction = "EGRESS"
#   allow { protocol = "icmp" }
#   allow {
#     protocol = "tcp"
#     ports    = ["80", "443"]
#   }
#   # target_tags = ["dataflow"]
#   destination_ranges = ["0.0.0.0/0"]
# }

# resource "google_notebooks_runtime" "runtime" {
#   name = "notebooks-runtime"
#   location = "us-east4"
#   access_config {
#     access_type = "SINGLE_USER"
#     runtime_owner = "hvu7470@hca.corpad.net"
#   }
#   virtual_machine {
#     virtual_machine_config {
#       machine_type = "n1-standard-4"
#       data_disk {
#         initialize_params {
#           disk_size_gb = "100"
#           disk_type = "PD_STANDARD"
#         }
#       }
#     }
#   }
# }
