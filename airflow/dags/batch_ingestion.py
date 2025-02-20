from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import json
import random
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


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
    for _ in range(100): 
        activity_type = random.choice(["walking", "running", "cycling"])
        steps = random.randint(1000, 20000)
        distance_km = round(steps * 0.0008, 2)  # Assuming 0.8m per step

        # Heart rate adjustment based on activity type
        if activity_type == "walking":
            heart_rate = random.randint(60, 100)
            calories_burned = round(random.uniform(50, 300), 2)
        elif activity_type == "running":
            heart_rate = random.randint(100, 160)
            calories_burned = round(random.uniform(200, 700), 2)
        else:  # cycling
            heart_rate = random.randint(90, 140)
            calories_burned = round(random.uniform(150, 500), 2)

        workout_duration_min = random.randint(10, 120)

        record = {
            "user_id": random.randint(1000, 9999),
            "steps": steps,
            "distance_km": distance_km,
            "heart_rate": heart_rate,
            "calories_burned": calories_burned,
            "activity_type": activity_type,
            "workout_duration_min": workout_duration_min,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        data.append(record)

    # Save the data to a local file in NDJSON format
    local_file_path = "/tmp/batch_fitness_data.json"
    with open(local_file_path, "w") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")  # Write each record as a separate line

    print(f"Data saved to {local_file_path} in NDJSON format")

# Define the DAG
with DAG(
    "batch_ingestion",
    default_args=default_args,
    schedule_interval="@monthly", 
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
        bucket="fitness-data-bucket",  
        mime_type="application/json",
        gcp_conn_id="google_cloud_default",
    )

    # Task 3: Load data from GCS to BigQuery
    load_to_bigquery = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket="fitness-data-bucket",
        source_objects=["batch_data/batch_fitness_data.json"],
        destination_project_dataset_table="fit-analytics-pipeline:fitness_data.fitness_metrics",
        source_format="NEWLINE_DELIMITED_JSON",
        autodetect=True,
        write_disposition="WRITE_APPEND",
        gcp_conn_id="google_cloud_default",  # Explicitly use the connection

    )

    # Define task dependencies
    generate_data >> upload_to_gcs >> load_to_bigquery
