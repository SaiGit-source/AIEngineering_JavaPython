import json
import os
from datetime import datetime
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_LOGS_FILE = BASE_DIR / "data" / "raw_logs.jsonl"

AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")

LOG_GROUP_NAME = "/banking/simulated-prod"
LOG_STREAM_NAME = "local-log-generator"

logs_client = boto3.client(
    "logs",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


def create_log_group_if_needed():
    try:
        logs_client.create_log_group(logGroupName=LOG_GROUP_NAME)
        print(f"Created log group: {LOG_GROUP_NAME}")
    except logs_client.exceptions.ResourceAlreadyExistsException:
        print(f"Log group already exists: {LOG_GROUP_NAME}")


def create_log_stream_if_needed():
    try:
        logs_client.create_log_stream(
            logGroupName=LOG_GROUP_NAME,
            logStreamName=LOG_STREAM_NAME
        )
        print(f"Created log stream: {LOG_STREAM_NAME}")
    except logs_client.exceptions.ResourceAlreadyExistsException:
        print(f"Log stream already exists: {LOG_STREAM_NAME}")


def iso_to_millis(timestamp_text):
    dt = datetime.fromisoformat(timestamp_text.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)


def load_log_events():
    events = []

    with open(RAW_LOGS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            log = json.loads(line)

            events.append({
                "timestamp": iso_to_millis(log["timestamp"]),
                "message": json.dumps(log)
            })

    events.sort(key=lambda event: event["timestamp"])
    return events


def push_logs_to_cloudwatch():
    create_log_group_if_needed()
    create_log_stream_if_needed()

    events = load_log_events()

    response = logs_client.put_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamName=LOG_STREAM_NAME,
        logEvents=events
    )

    print(f"Pushed {len(events)} log events to CloudWatch")
    print(response)


if __name__ == "__main__":
    push_logs_to_cloudwatch()