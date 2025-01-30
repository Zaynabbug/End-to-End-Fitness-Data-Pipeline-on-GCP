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

resource "google_pubsub_topic" "fitness_topic" {
  name = "fitness-topic"
}

resource "google_pubsub_subscription" "fitness_subscription" {
  name  = "fitness-subscription"
  topic = google_pubsub_topic.fitness_topic.id
}
