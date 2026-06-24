import base64
import gzip
import json


def lambda_handler(event, context):
    compressed_payload = base64.b64decode(event["awslogs"]["data"])
    uncompressed_payload = gzip.decompress(compressed_payload)
    log_data = json.loads(uncompressed_payload)

    print("Decoded CloudWatch payload:")
    print(json.dumps(log_data, indent=2))

    for log_event in log_data.get("logEvents", []):
        message = log_event.get("message")
        print("Log message:", message)

    return {
        "statusCode": 200,
        "body": "CloudWatch logs received successfully"
    }