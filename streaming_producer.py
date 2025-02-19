import os
import time
import json
import random
from google.cloud import pubsub_v1
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/zayna/.gcp/fit-analytics-pipeline-4263c3d629fe.json"

# Set up Pub/Sub client
project_id = "fit-analytics-pipeline"  # Replace with your GCP project ID
topic_id = "fitness-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Function to generate random fitness data
def generate_fitness_data():
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

    return {
        "user_id": random.randint(1000, 9999),
        "steps": steps,
        "distance_km": distance_km,
        "heart_rate": heart_rate,
        "calories_burned": calories_burned,
        "activity_type": activity_type,
        "workout_duration_min": workout_duration_min,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

# Publish messages to Pub/Sub
def publish_messages():
    while True:
        data = generate_fitness_data()
        message_json = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, message_json)
        print(f"Published: {data}")
        time.sleep(25)  # Simulate data every 25 seconds

if __name__ == "__main__":
    publish_messages()