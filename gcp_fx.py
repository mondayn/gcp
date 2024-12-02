
#region imports
import pydata_google_auth
import os
import json
from google.cloud import storage
import pandas as pd
from io import BytesIO
#endregion

#region globals
CREDENTIALS = pydata_google_auth.get_user_credentials('https://www.googleapis.com/auth/cloud-platform')

def get_project_id():
    ''' assume windows '''
    adc_file=os.environ['USERPROFILE']+r'\AppData\Roaming\gcloud\application_default_credentials.json'
    with open(adc_file, "r") as file:
        data = json.load(file)  
    return data['quota_project_id']
PROJECT_ID=get_project_id()

# import configparser
# cp = configparser.ConfigParser()
# cp.read('config.ini')
# PROJECT_ID = cp['GCP']['PROJECT_ID']

#endregion

#region storage
def get_bucket(bucket_id=PROJECT_ID + '_b1'):
    ''' to do: other buckets, create bucket if not exists '''
    return storage.Client(PROJECT_ID).bucket(bucket_id)

def upload_file(file='cal.txt',bucket=get_bucket()):
    bucket.upload_from_filename(file)
    print(f'uploaded {file}')

def download_blob_as_bytes(blob):
    return BytesIO(blob.download_as_bytes())
#endregion

#region big query
import pandas_gbq
import pandas as pd
from google.cloud import bigquery

def print_meta_data(_df):
    ''' helper fx
    '''
    print('shape =',_df.shape)
    print('columns = ',list(_df.columns))
    return _df

def query_bq(sql):

    gbq_params = {
        'query':sql
        ,'project_id': PROJECT_ID
        ,'credentials': CREDENTIALS
    }
    # print(f'gbq_params={gbq_params}')
    return (
        pd.read_gbq(**gbq_params)
        .pipe(print_meta_data)
    )

def delete_bq_table(dataset_name, table_name):
    client = bigquery.Client(PROJECT_ID,CREDENTIALS)
    table_id = f'{dataset_name}.{table_name}'
    client.delete_table(table_id, not_found_ok=True) 
    print("Deleted table '{}'.".format(table_id))
#endregion


if __name__ == '__main__':
    print(get_bucket('test2'))
    