import boto3
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/912753427807/trying-sqs"
BUCKET = "weather-bucket-for-verisk-internship"
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("WeatherSnapshots")

HIGH_TEMP_THRESHOLD = float(os.getenv("HIGH_TEMP_THRESHOLD", 35))
LOW_TEMP_THRESHOLD = float(os.getenv("LOW_TEMP_THRESHOLD", 5))

sqs = boto3.client("sqs", region_name=AWS_REGION)
s3 = boto3.client("s3")

def upload_to_s3(city_name, data, timestamp):
    key = f"weather_data/{city_name}/{timestamp}.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )
    print(f"[Info] Uploaded data for {city_name} to S3")


def store_in_dynamodb(city, timestamp, data):
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    weather_main = data["weather"][0]["main"]

    if temp > HIGH_TEMP_THRESHOLD:
        alert = "HOT"
    elif temp < LOW_TEMP_THRESHOLD:
        alert = "COLD"
    else:
        alert = "NORMAL"

    table.put_item(
        Item={
            "city": city,                    
            "timestamp": str(timestamp),       # DynamoDB expects string
            "temp": Decimal(str(temp)),        # Convert float to Decimal
            "humidity": Decimal(str(humidity)),
            "pressure": Decimal(str(pressure)),
            "weather_main": weather_main,
            "alert_level": alert
        }
    )

    print(f"[Info] Stored snapshot in DynamoDB for {city} @ {timestamp}")

def process_message(message):
    """
    Process a single SQS message: validate, upload to S3, store in DynamoDB, and log alerts.
    """
    try:
        # Parse message
        body = json.loads(message.get("Body", "{}"))

        # Validate required keys
        if "city_key" not in body or "city_query" not in body or "data" not in body:
            print(f"[Warning] Skipping incomplete message: {body}")
            return

        city_key = body["city_key"]
        city_query = body["city_query"]
        data = body["data"]

        # Extract temperature for alerts
        temp = data.get("main", {}).get("temp")
        if temp is not None:
            if temp > HIGH_TEMP_THRESHOLD:
                print(f"[ALERT] {city_query} is hot: {temp}°C")
            elif temp < LOW_TEMP_THRESHOLD:
                print(f"[ALERT] {city_query} is cold: {temp}°C")

        # Timestamp for S3 and DynamoDB
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H")

        # Upload JSON to S3
        try:
            upload_to_s3(city_key, data, timestamp)
        except Exception as e:
            print(f"[Warning] Failed to upload to S3 for {city_key}: {e}")

        # Store in DynamoDB
        try:
            store_in_dynamodb(city_key, timestamp, data)
        except Exception as e:
            print(f"[Warning] Failed to store in DynamoDB for {city_key}: {e}")

    except json.JSONDecodeError as e:
        print(f"[Warning] Malformed message skipped: {message.get('Body')}")
    except Exception as e:
        print(f"[Error] Unexpected error processing message: {e}")



def main():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=20
        )

        messages = response.get("Messages", [])
        for message in messages:
            try:
                process_message(message)

                # Delete message after processing
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"]
                )
            except Exception as e:
                print(f"[Error] Processing failed: {e}")

        time.sleep(2)


if __name__ == "__main__":
    main()
