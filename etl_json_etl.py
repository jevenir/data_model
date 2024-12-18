from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime
import pandas as pd
import requests
from google.cloud import storage

# default args for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

# DAG
with DAG(
    "etl_to_bigquery",
    default_args=default_args,
    description="ETL pipeline to BigQuery",
    schedule_interval="@daily",
    start_date=datetime(2024, 12, 18),
    catchup=False,
) as dag:

# Extract data
    def extract_data(**kwargs):
        url = "https://github.com/jevenir/data_model/blob/main/etl.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        df.to_csv("/tmp/extracted_data.csv", index=False)
    
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

# Transform data
    def transform_data(**kwargs):
        df = pd.read_csv("/tmp/extracted_data.csv")
        df = df.dropna()
        df["date"] = pd.to_datetime(df["date"])
        df.to_csv("/tmp/transformed_data.csv", index=False)
    
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

# Load data
    load_task = BigQueryInsertJobOperator(
        task_id="load_data_to_bigquery",
        configuration={
            "load": {
                "sourceUris": ["gs://jevgenir_bucket/transformed_data.csv"],
                "destinationTable": {
                    "projectId": "evocative-ethos-370813",
                    "datasetId": "jevgenir_sandbox",
                    "tableId": "test_table",
                },
                "sourceFormat": "CSV",
                "writeDisposition": "WRITE_TRUNCATE",
            }
        },
        location="EU",
    )

# Task dependencies
    extract_task >> transform_task >> load_task
