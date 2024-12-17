import apache_beam as beam
from apache_beam.io.gcp.bigquery import WriteToBigQuery
from gcp_fx import PROJECT_ID

# Define a schema for the target BigQuery table
table_schema = {
    'fields': [
        {'name': 'ride_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'distance', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'timestamp', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}
    ]
}

with beam.Pipeline() as pipeline:
    (
        pipeline
        | 'Create Data' >> beam.Create([
            {'ride_id': '1234', 'distance': 10.5, 'timestamp': '2024-06-17T12:00:00Z'},
            {'ride_id': '5678', 'distance': 7.3, 'timestamp': '2024-06-17T12:05:00Z'}
        ])
        | 'Write to BigQuery' >> WriteToBigQuery(
            table=f'{PROJECT_ID}:dataflow.test',
            schema=table_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            method='FILE_LOADS',
            custom_gcs_temp_location='gs://dataflow-staging-us-central1-925178969788/temp/'
        )
    )
