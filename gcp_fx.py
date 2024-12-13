import os
import json
from google.cloud import storage, bigquery, pubsub_v1
import pandas as pd

import configparser
cp = configparser.ConfigParser()
cp.read('config/config.ini')

import pydata_google_auth
CREDENTIALS = pydata_google_auth.get_user_credentials('https://www.googleapis.com/auth/cloud-platform')

def get_project_id():
    # windows
    # adc_file=os.environ['USERPROFILE']+r'\AppData\Roaming\gcloud\application_default_credentials.json'
    # with open(adc_file, "r") as file:
    #     data = json.load(file)  
    # return data['quota_project_id']
    return cp['GCP']['PROJECT_ID']
PROJECT_ID=get_project_id()


#region storage
def get_bucket(bucket_id=PROJECT_ID + '_b1'):
    bucket = storage.Client(PROJECT_ID).bucket(bucket_id)
    if not bucket.exists():
        bucket.create(bucket_id)
    return bucket

def upload_file(file='cal.txt',bucket=get_bucket()):
    bucket.upload_from_filename(file)
    print(f'uploaded {file}')

def blob_str(blob_name,bucket=get_bucket()):
    blob = bucket.blob(blob_name) 
    if blob.exists():
        return blob.download_as_bytes().decode()
#endregion

#region big query
def print_meta_data(_df):
    print('shape =',_df.shape)
    print('columns = ',list(_df.columns))
    return _df

def query_bq(sql='select session_user()')->pd.DataFrame:
    client = bigquery.Client(PROJECT_ID)
    return client.query(sql).to_dataframe().pipe(print_meta_data)

def delete_bq_table(dataset_name, table_name):
    client = bigquery.Client(PROJECT_ID)
    table_id = f'{dataset_name}.{table_name}'
    client.delete_table(table_id, not_found_ok=True) 
    print("Deleted table '{}'.".format(table_id))
# endregion

#region pubsub
pub = pubsub_v1.PublisherClient()
sub = pubsub_v1.SubscriberClient()
project_kv={"project": f'projects/{PROJECT_ID}'}

def ls_topics():
    return [x.name for x in pub.list_topics(project_kv)]

def rm_topics():
    for x in ls_topics():
        pub.delete_topic({'topic':x})

def ls_subs():
    return [x.name for x in sub.list_subscriptions(project_kv)]

def rm_subs():
    for x in ls_subs():
        sub.delete_subscription({'subscription':x})

def mk_topic(topic_name):
    topic_path = f'projects/{PROJECT_ID}/topics/{topic_name}'
    pub.create_topic(name=topic_path)
    return topic_path

def mk_sub(sub_name,topic_path):
    ''' this is fun
        mk_sub('sub1','projects/pubsub-public-data/topics/taxirides-realtime')
     '''
    sub_path = f'projects/{PROJECT_ID}/subscriptions/{sub_name}'
    sub.create_subscription(name=sub_path,topic=topic_path)
    return sub_path

def sub_pull(subscription):
    ''' usage:
        pub.publish(topic, b'message!', some_key='e_value')
        sub_pull(subscription)
     '''
    response = sub.pull(request={'subscription':subscription,'max_messages':5}, timeout=20)
    def handle_msg(r):
        print(f'data = {r.message.data.decode()}\t\t,attributes={r.message.attributes}')
        return r.ack_id
    ack_ids = list(map(handle_msg,response.received_messages))
    if ack_ids:
        sub.acknowledge(request={'subscription': subscription,'ack_ids':ack_ids})

def publish_msg(topic_name,msg):
    topic_path=f'projects/{PROJECT_ID}/topics/{topic_name}'
    pub.publish(topic_path,msg.encode("utf-8"))
#endregion


if __name__ == '__main__':
    print(PROJECT_ID)
    # sql = 'SELECT * FROM `bigquery-public-data.pypi.simple_requests` WHERE TIMESTAMP_TRUNC(timestamp, DAY) = TIMESTAMP("2024-12-08") LIMIT 1000'
    # print(query_bq(sql))

    