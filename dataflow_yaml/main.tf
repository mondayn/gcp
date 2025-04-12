provider "google" {
  project = var.project_id
}


resource "google_storage_bucket" "staging_bucket" {
  name                        = "${var.project_id}-staging"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}


/************* WORD COUNT EXAMPLE 

resource "google_storage_bucket" "io_bucket" {
  name                        = "${var.project_id}-io"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_dataflow_job" "wordcount_job" {
  name              = "wordcount-dataflow-job"
  region            = var.region
  template_gcs_path = "gs://dataflow-templates/latest/Word_Count"
  temp_gcs_location = "gs://${google_storage_bucket.staging_bucket.name}/tmp"
  ip_configuration  = "WORKER_IP_PRIVATE"

  parameters = {
    inputFile = "gs://dataflow-samples/shakespeare/kinglear.txt"
    output    = "gs://${google_storage_bucket.io_bucket.name}/wordcount_output"
  }

  network    = google_compute_network.my_network.id
  subnetwork = google_compute_subnetwork.my_subnet.self_link
}

*******************/

