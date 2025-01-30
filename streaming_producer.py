import time
import json
import random
from google.cloud import pubsub_v1

# Set up Pub/Sub client
project_id = "fit-analytics-pipeline"  # Replace with your GCP project ID
topic_id = "fitness-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Function to generate random fitness data
def generate_fitness_data():
    return {
        "user_id": random.randint(1000, 9999),
        "steps": random.randint(1000, 20000),
        "heart_rate": random.randint(60, 180),
        "calories_burned": round(random.uniform(50, 800), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

# Publish messages to Pub/Sub
def publish_messages():
    while True:
        data = generate_fitness_data()
        message_json = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, message_json)
        print(f"Published: {data}")
        time.sleep(5)  # Simulate data every 5 seconds

if __name__ == "__main__":
    publish_messages()
