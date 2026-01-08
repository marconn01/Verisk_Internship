import boto3
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/912753427807/trying-sqs"

CITIES = {
    "kathmandu": "Kathmandu,NP",
    "london": "London,GB",
    "newyork": "New York,US",
}

sqs = boto3.client("sqs", region_name=AWS_REGION)

def fetch_weather(city_query):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city_query,
                "appid": API_KEY,
                "units": "metric"
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[Error] Failed to fetch weather for {city_query}: {e}")
        return None

def push_to_sqs(city_key, city_query, data):
    message = {
        "city_key": city_key,
        "city_query": city_query,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }

    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    print(f"[Info] Sent weather data for {city_query} to SQS")

def main():
    for city_key, city_query in CITIES.items():
        data = fetch_weather(city_query)
        if data:
            push_to_sqs(city_key, city_query, data)

if __name__ == "__main__":
    main()
