import os
import json
from google.cloud import storage, bigquery, pubsub_v1, run_v2
import pandas as pd
import pydata_google_auth
from cytoolz import thread_first,thread_last


#region initialize

import configparser
cp = configparser.ConfigParser()
cp.read('config/config.ini')
PROJECT_ID = cp['GCP']['PROJECT_ID']
REGION_ID = cp['GCP']['REGION_ID']

CREDENTIALS = pydata_google_auth.get_user_credentials('https://www.googleapis.com/auth/cloud-platform')

# def get_project_id():
    # windows
    # adc_file=os.environ['USERPROFILE']+r'\AppData\Roaming\gcloud\application_default_credentials.json'
    # with open(adc_file, "r") as file:
    #     data = json.load(file)  
    # return data['quota_project_id']
#endregion

#region storage

def list_buckets():
    client = storage.Client()
    buckets = list(map(lambda x: x.name,client.list_buckets()))
    print(f'there are {len(buckets)} buckets: {buckets}')

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
class Pubs():
    def __init__(self):
        self.client = pubsub_v1.PublisherClient()
        self.projects = self.client.common_project_path(PROJECT_ID)
        self.folder = self.projects + '/topics/'

    def __getitem__(self,name): 
        return self.folder + name

    def ls(self):
        return [x.name for x in self.client.list_topics({"project": self.projects})]

    def remove(self,topic): 
        self.client.delete_topic({'topic':self.folder+topic})

    def remove_all(self):
        for x in self.ls():
            self.client.delete_topic({'topic':x})

    def create(self,name):
        topic_path = self.folder + name
        return self.client.create_topic(name=topic_path)

    def send(self,topic,msg):
        self.client.publish(self.folder + topic, msg.encode("utf-8"))


class Subs():
    def __init__(self):
        self.client = pubsub_v1.SubscriberClient()
        self.projects = self.client.common_project_path(PROJECT_ID)
        self.folder = self.projects + '/subscriptions/'
    
    def __getitem__(self,name): 
        return self.folder + name

    def ls(self):
        return [x.name for x in self.client.list_subscriptions({"project":self.projects})]

    def remove(self,sub):
        subscription = self.folder + sub
        print('removing ',subscription)
        self.client.delete_subscription({'subscription':subscription})

    def remove_all(self):
        for x in self.ls():
            self.client.delete_subscription({'subscription':x})

    def create(self,sub_name,topic):
        ''' would be fun 'projects/pubsub-public-data/topics/taxirides-realtime'
        '''
        self.name = self.folder + sub_name
        return self.client.create_subscription(name=self.name,topic=topic)

    def pull(self,sub_name):
        ''' Subs()['name'].pull() 
        '''
        subscription = self.folder + sub_name
        response = self.client.pull(request={'subscription':subscription,'max_messages':5}, timeout=20)
        def handle_msg(r):
            print(f'data = {r.message.data.decode()}\t\t,attributes={r.message.attributes}')
            return r.ack_id
        ack_ids = list(map(handle_msg,response.received_messages))
        if ack_ids:
            self.client.acknowledge(request={'subscription': subscription,'ack_ids':ack_ids})

#endregion

#region cloud run fx
def sample_list_services():
    client = run_v2.ServicesClient()
    request = run_v2.ListServicesRequest(parent=f"projects/{PROJECT_ID}/locations/us-central1")
    page_result = client.list_services(request)
    print(list(map(lambda x: x.name,page_result)))

#endregion
if __name__ == '__main__':
    print(PROJECT_ID)
    print(REGION_ID)
    list_buckets()
    # client = run_v2.ServicesClient(PROJECT_ID)
    # print(client.list_services())

    