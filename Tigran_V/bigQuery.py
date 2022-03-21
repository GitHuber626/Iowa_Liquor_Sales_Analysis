from dataclasses import dataclass
from google.cloud import bigquery
import os
import pandas as pd
import pyarrow


pd.set_option("display.max_columns",10)
path = '/Users/tiko/Downloads/BQ_cred.json'


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

project = 'liquor-store-analysis'
dataset = 'liquor-store-analysis'

client = bigquery.Client(project=project)
df_sql = client.dataset(dataset)

qr = client.query("""

SELECT * FROM 
`liquor-store-analysis.Liquor_Dataset.TABLE1`
LIMIT 20
""")

results = qr.result()
df = results.to_dataframe()
print(df)
# name_group_query = """
# SELECT * FROM `bigquery-public-data.iowa_liquor_sales.sales` 
# LIMIT 20 OFFSET 2;
# """

# client.query(name_group_query)