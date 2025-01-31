from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import json
import random

# Define default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 30),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define batch data generation function
def generate_batch_data():
    data = []
    for _ in range(100):  # Generate 100 records
        record = {
            "user_id": random.randint(1000, 9999),
            "steps": random.randint(1000, 20000),
            "heart_rate": random.randint(60, 180),
            "calories_burned": round(random.uniform(50, 800), 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        data.append(record)

    with open("/tmp/batch_fitness_data.json", "w") as f:
        json.dump(data, f)

# Define the DAG
with DAG(
    "batch_ingestion",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Task 1: Generate batch fitness data
    generate_data = PythonOperator(
        task_id="generate_batch_data",
        python_callable=generate_batch_data,
    )

    # Task 2: Upload the batch data to Cloud Storage
    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src="/tmp/batch_fitness_data.json",
        dst="batch_data/batch_fitness_data.json",
        bucket="fitness-data-bucket",  # Replace with your GCS bucket name
        mime_type="application/json",
    )

    # Task 3: Load data from GCS to BigQuery
    load_to_bigquery = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket="fitness-data-bucket",
        source_objects=["batch_data/batch_fitness_data.json"],
        destination_project_dataset_table="fitness-data-pipeline:fitness_data.fitness_metrics",
        source_format="NEWLINE_DELIMITED_JSON",
        autodetect=True,
        write_disposition="WRITE_APPEND",
    )

    # Define task dependencies
    generate_data >> upload_to_gcs >> load_to_bigquery
