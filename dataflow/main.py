import apache_beam as beam
import logging
import json

# from apache_beam.io.gcp.bigquery import WriteToBigQuery
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from google.cloud import storage

PROJECT_ID = storage.Client().project
REGION = 'us-east4' #'us-central1'

# temp_location = f'gs://{PROJECT_ID}_dataflow_simple/temp/'

# bucket_name=f'{PROJECT_ID}_b2'
# blob_name='test.txt'
# file_name = f'gs://{bucket_name}/{blob_name}'
# storage.Client().bucket(bucket_name).blob(blob_name).upload_from_string('test\nthis\nout')

subscription=f'projects/{PROJECT_ID}/subscriptions/taxi'
destination=f'{PROJECT_ID}.taxirides.realtime'

def parse_pubsub_message(message):
    """Parse the Pub/Sub message from JSON format."""
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}

def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True
    # CustomPipelineOptions(
    #     runner='DataflowRunner',
    #     job_name='dataflow-simple',
    #     project=PROJECT_ID,
    #     region=REGION,
    #     # network='dataflow-east4-network',
    #     network='my-dataflow-network',
    #     subnetwork=f'regions/{REGION}/subnetworks/dataflow-east4-network',
    #     use_public_ips=False

    # )
    p = beam.Pipeline(options=options)
    (   p
        # | 'Create Data' >> beam.Create([
        #     {'ride_id': '1234', 'distance': 10.5, 'timestamp': '2024-06-17T12:00:00Z'},
        #     {'ride_id': '5678', 'distance': 7.3, 'timestamp': '2024-06-17T12:05:00Z'}
        # ])

        # | 'Read from GCS' >> beam.io.ReadFromText(options.input)
        | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription=subscription)
        | "Decode Messages" >> beam.Map(lambda x: x.decode('utf-8'))  # Decode from bytes to string
        | "Parse JSON" >> beam.Map(parse_pubsub_message)  # Parse JSON
        | "Filter Valid Messages" >> beam.Filter(lambda x: x is not None)  # Remove invalid messages
        | "Write to BigQuery" >> beam.io.WriteToBigQuery(
            table=destination,
            # schema={
            #     'fields': [
            #         {'name': 'ride_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            #         {'name': 'point_idx', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            #         {'name': 'latitude', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            #         {'name': 'longitude', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            #         {'name': 'timestamp', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            #         {'name': 'meter_reading', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            #         {'name': 'meter_increment', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            #         {'name': 'ride_status', 'type': 'STRING', 'mode': 'NULLABLE'},
            #         {'name': 'passenger_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},                
            #     ]
            # },
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            # create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
        # | "PrintLog" >> beam.Map(logging.info)
        # | "Print Messages" >> beam.Map(print)  # Print messages to stdout
    )    
    p.run().wait_until_finish()

if __name__ == "__main__":
    run()
    logging.getLogger().setLevel(logging.INFO)
    pass

# print(storage.Client().bucket(bucket_name).blob(blob_name).download_as_text())