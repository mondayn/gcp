import functions_framework
from google.cloud import storage
import datetime

@functions_framework.cloud_event
def update_bucket(cloud_event):
    s = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
    PROJECT_ID='hca-hvu7470-202411221829-sbx'
    bucket = storage.Client(PROJECT_ID).bucket('hca-hvu7470-202411221829-sbx_b1')
    bucket.blob('test.txt').upload_from_string(s)
