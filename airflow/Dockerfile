# Start from the official Airflow image
FROM apache/airflow:latest

# Switch to airflow user before installing dbt
USER airflow

# Install dbt for BigQuery
RUN pip install --no-cache-dir dbt-bigquery
