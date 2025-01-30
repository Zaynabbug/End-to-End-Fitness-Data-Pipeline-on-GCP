import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from google.cloud import bigquery

# Define project details
PROJECT_ID = "fit-analytics-pipeline"  # Replace with your GCP Project ID
TOPIC = f"projects/{PROJECT_ID}/topics/fitness-topic"
TABLE_ID = f"{PROJECT_ID}:fitness_data.fitness_metrics"

# Define the transformation function
def parse_pubsub_message(message):
    data = json.loads(message.decode("utf-8"))
    data["timestamp"] = beam.Row(timestamp=data["timestamp"])  # Ensure correct format
    return data

# Define pipeline options
pipeline_options = PipelineOptions(
    streaming=True,
    project=PROJECT_ID,
    region="us-central1",
    runner="DataflowRunner",
    temp_location=f"gs://{PROJECT_ID}-temp/",
)

# Define the Beam pipeline
with beam.Pipeline(options=pipeline_options) as pipeline:
    (
        pipeline
        | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=TOPIC)
        | "Parse JSON" >> beam.Map(parse_pubsub_message)
        | "Write to BigQuery" >> beam.io.WriteToBigQuery(
            TABLE_ID,
            schema="user_id:INTEGER, steps:INTEGER, heart_rate:INTEGER, calories_burned:FLOAT, timestamp:TIMESTAMP",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )
