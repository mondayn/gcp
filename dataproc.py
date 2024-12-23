from google.auth import default
credentials, PROJECT_ID = default()

import pandas as pd
file = f'gs://{PROJECT_ID}_b3/fortune1000_2024.parquet'
data = [(i.Company,) for i in pd.read_parquet(file).itertuples()]
len(data)

from pyspark.sql import SparkSession
from pyspark.sql.functions import levenshtein, col

# Initialize SparkSession
spark = (SparkSession.builder 
    .appName("Levenshtein Example") \
    # .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    # .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "gs://{PROJECT_ID}_b3/adc.json")
    .getOrCreate()
        )


(
    spark.createDataFrame(data,['company'])
    .crossJoin(spark.createDataFrame(data,['otherco']))
    .withColumn("lev_dist", levenshtein(col("company"), col("otherco")))
    .filter("lev_dist between 0 and 10 ")
    # .show(10)
    .count()
)