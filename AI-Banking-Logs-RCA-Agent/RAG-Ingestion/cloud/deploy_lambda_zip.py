import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ZIP_FILE = BASE_DIR / "lambda_build" / "banking-log-ingestion-lambda.zip"

AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")
FUNCTION_NAME = "banking-log-ingestion-lambda"

lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

if not ZIP_FILE.exists():
    raise FileNotFoundError(f"Zip file not found: {ZIP_FILE}")

with open(ZIP_FILE, "rb") as file:
    zip_bytes = file.read()

response = lambda_client.update_function_code(
    FunctionName=FUNCTION_NAME,
    ZipFile=zip_bytes
)

print("Lambda zip deployed successfully")
print("Function:", response["FunctionName"])
print("Last modified:", response["LastModified"])
print("Code SHA256:", response["CodeSha256"])