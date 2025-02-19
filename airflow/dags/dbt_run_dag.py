from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 1),  # Start date for the DAG
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    "dbt_run",
    default_args=default_args,
    schedule_interval="*/20 * * * *",  # Run every 10 minutes
    catchup=False,
) as dag:

    # Task: Run dbt transformation
    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /fitness-data-pipeline/fitness_dbt && dbt run",
    )
    
    run_dbt 