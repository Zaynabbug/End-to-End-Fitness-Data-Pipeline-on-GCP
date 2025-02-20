terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "fit-analytics-pipeline"  # Replace with your actual GCP project ID
  region  = "us-central1"
}

# Create Pub/Sub topic
resource "google_pubsub_topic" "fitness_topic" {
  name = "fitness-topic"
}

# Create Pub/Sub subscription that writes to BigQuery
resource "google_pubsub_subscription" "fitness_subscription" {
  name  = "fitness-subscription"
  topic = google_pubsub_topic.fitness_topic.id

  bigquery_config {
    table            = "fit-analytics-pipeline.fitness_data.fitness_metrics"
    write_metadata   = false  
  }

  ack_deadline_seconds = 60
}
