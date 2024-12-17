from google.cloud import storage
import json

import google.auth
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials

import logging
from google.cloud import logging as cloud_logging

# import datetime
import base64
import psycopg2
import os

client = cloud_logging.Client()
client.setup_logging()

logger = logging.getLogger("cloud-run-logger")
logger.info('starting')

def get_iam_token():
    """Generates an IAM token for the Cloud SQL IAM user."""
    credentials, _ = google.auth.default()
    auth_request = Request()
    credentials.refresh(auth_request)
    return credentials.token

def get_db_config():
    ''' get user, host from a blob stored by gcp_fx '''
    bucket_name = storage.Client().project+'_b1'
    bucket = storage.Client().bucket(bucket_name)
    return json.loads(bucket.blob('postgres').download_as_bytes().decode())

def entry_point(event,context):    
    db_config = get_db_config()
    db_config['password'] = get_iam_token()
    print(db_config)
    logging.info(f'db_config is {db_config}')

    msg = 'None found'
    if 'data' in event:
        msg = base64.b64decode(event["data"]).decode("utf-8")
    logging.info(f'msg is {msg}')
    
    with psycopg2.connect(**db_config) as con:
        cursor=con.cursor()
        sql = f"insert into postgres.public.pubsub_messages values({context.event_id},CURRENT_TIMESTAMP,'{msg}')"
        results=cursor.execute(sql)
        con.commit()
        cursor.close()

if __name__=='__main__':
    entry_point(None,None)

