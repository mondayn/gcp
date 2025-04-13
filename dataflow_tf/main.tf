provider "google" {
  project = var.project_id
}

resource "google_storage_bucket" "io_bucket" {
  name                        = "${var.project_id}-io"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "staging_bucket" {
  name                        = "${var.project_id}-staging"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "bigquery_dataset" {
  dataset_id = "dataflow"
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "bigquery_table" {
  dataset_id = google_bigquery_dataset.bigquery_dataset.dataset_id
  table_id   = "random"
  deletion_protection = false
  schema     = <<EOF
[
  {"name": "dim","type": "STRING","mode": "NULLABLE"},
  {"name": "amt","type": "INTEGER","mode": "NULLABLE"},
  {"name": "msr","type": "INTEGER","mode": "NULLABLE"}
]
EOF
}

resource "google_bigquery_table" "bigquery_table_err" {
  dataset_id = google_bigquery_dataset.bigquery_dataset.dataset_id
  table_id   = "random_err"
  deletion_protection = false

  schema = <<EOF
[
  {"name": "RawContent","type": "STRING"},
  {"name": "ErrorMsg","type": "STRING"}
]
EOF
}

resource "google_dataflow_job" "dataflow_job" {
  name              = "storage-to-bq"
  region            = var.region
  template_gcs_path = "gs://dataflow-templates/latest/GCS_CSV_to_BigQuery"
  temp_gcs_location = "gs://${google_storage_bucket.staging_bucket.name}/tmp"
  ip_configuration  = "WORKER_IP_PRIVATE"

  parameters = {
    inputFilePattern                  = "gs://${google_storage_bucket.io_bucket.name}/random.csv"
    schemaJSONPath                    = "gs://${google_storage_bucket.io_bucket.name}/schema.json"
    outputTable                       = "hca-hvu7470-202504041334-sbx.dataflow.random"
    badRecordsOutputTable             = "hca-hvu7470-202504041334-sbx.dataflow.random_err"
    bigQueryLoadingTemporaryDirectory = "gs://${google_storage_bucket.staging_bucket.name}/tmp"
    delimiter                         = ","
    csvFormat                         = "Default"
    containsHeaders                   = true
  }
  network    = google_compute_network.my_network.id
  subnetwork = google_compute_subnetwork.my_subnet.self_link
  max_workers = 1

}






# resource "google_pubsub_subscription" "taxi-subscription" {
#   name                       = "my-pubsub-subscription"
#   topic                      = "projects/pubsub-public-data/topics/taxirides-realtime"
#   message_retention_duration = "1200s"
# }




/************* WORD COUNT EXAMPLE 


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