import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "raw_logs.jsonl"

logs = [
    # TRACE-10045: fraud-service root cause
    {
        "timestamp": "2026-06-22T10:15:29Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10045",
        "transactionId": "TXN-789",
        "service": "auth-service",
        "level": "INFO",
        "eventType": "APPLICATION_LOG",
        "errorCode": "NONE",
        "latencyMs": 120,
        "message": "Token validation successful"
    },
    {
        "timestamp": "2026-06-22T10:15:30Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10045",
        "transactionId": "TXN-789",
        "service": "account-service",
        "level": "INFO",
        "eventType": "APPLICATION_LOG",
        "errorCode": "NONE",
        "latencyMs": 210,
        "message": "Account balance check successful"
    },
    {
        "timestamp": "2026-06-22T10:15:31Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10045",
        "transactionId": "TXN-789",
        "service": "payment-service",
        "level": "ERROR",
        "eventType": "APPLICATION_ERROR",
        "errorCode": "FRAUD_TIMEOUT",
        "latencyMs": 4300,
        "message": "Payment failed due to fraud-service timeout"
    },
    {
        "timestamp": "2026-06-22T10:15:33Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10045",
        "transactionId": "TXN-789",
        "service": "fraud-service",
        "level": "ERROR",
        "eventType": "READINESS_PROBE_FAILED",
        "errorCode": "SERVICE_UNHEALTHY",
        "latencyMs": 4200,
        "message": "Readiness probe failed: /health returned 503"
    },
    {
        "timestamp": "2026-06-22T10:15:34Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10045",
        "transactionId": "TXN-789",
        "service": "fraud-service",
        "level": "WARN",
        "eventType": "POD_RESTARTED",
        "errorCode": "POD_RESTARTED",
        "latencyMs": 0,
        "message": "fraud-service pod restarted after repeated health check failures"
    },

    # TRACE-10046: account-service DB root cause
    {
        "timestamp": "2026-06-22T10:17:29Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10046",
        "transactionId": "TXN-790",
        "service": "auth-service",
        "level": "INFO",
        "eventType": "APPLICATION_LOG",
        "errorCode": "NONE",
        "latencyMs": 105,
        "message": "Token validation successful"
    },
    {
        "timestamp": "2026-06-22T10:17:30Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10046",
        "transactionId": "TXN-790",
        "service": "account-service",
        "level": "ERROR",
        "eventType": "APPLICATION_ERROR",
        "errorCode": "DB_CONNECTION_ERROR",
        "latencyMs": 5100,
        "message": "Account balance lookup failed because database connection timed out"
    },
    {
        "timestamp": "2026-06-22T10:17:31Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10046",
        "transactionId": "TXN-790",
        "service": "payment-service",
        "level": "ERROR",
        "eventType": "APPLICATION_ERROR",
        "errorCode": "BALANCE_CHECK_FAILED",
        "latencyMs": 5200,
        "message": "Payment failed because account balance could not be verified"
    },
    {
        "timestamp": "2026-06-22T10:17:32Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10046",
        "transactionId": "TXN-790",
        "service": "account-service",
        "level": "ERROR",
        "eventType": "DATABASE_ERROR",
        "errorCode": "DB_POOL_EXHAUSTED",
        "latencyMs": 5000,
        "message": "Connection pool exhausted while connecting to account database"
    },

    # TRACE-10047: payment gateway timeout
    {
        "timestamp": "2026-06-22T10:20:10Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10047",
        "transactionId": "TXN-791",
        "service": "payment-service",
        "level": "ERROR",
        "eventType": "APPLICATION_ERROR",
        "errorCode": "GATEWAY_TIMEOUT",
        "latencyMs": 6200,
        "message": "Payment authorization failed because payment-gateway-service timed out"
    },
    {
        "timestamp": "2026-06-22T10:20:11Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10047",
        "transactionId": "TXN-791",
        "service": "payment-gateway-service",
        "level": "ERROR",
        "eventType": "DOWNSTREAM_TIMEOUT",
        "errorCode": "AUTH_PROVIDER_TIMEOUT",
        "latencyMs": 6100,
        "message": "External authorization provider did not respond within timeout"
    },

    # TRACE-10048: notification failure
    {
        "timestamp": "2026-06-22T10:23:40Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10048",
        "transactionId": "TXN-792",
        "service": "payment-service",
        "level": "INFO",
        "eventType": "APPLICATION_LOG",
        "errorCode": "NONE",
        "latencyMs": 300,
        "message": "Payment completed successfully"
    },
    {
        "timestamp": "2026-06-22T10:23:41Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10048",
        "transactionId": "TXN-792",
        "service": "notification-service",
        "level": "ERROR",
        "eventType": "QUEUE_ERROR",
        "errorCode": "QUEUE_PUBLISH_FAILED",
        "latencyMs": 950,
        "message": "Failed to publish payment confirmation message to notification queue"
    },

    # TRACE-10049: healthy transaction
    {
        "timestamp": "2026-06-22T10:25:10Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10049",
        "transactionId": "TXN-793",
        "service": "auth-service",
        "level": "INFO",
        "eventType": "APPLICATION_LOG",
        "errorCode": "NONE",
        "latencyMs": 90,
        "message": "Token validation successful"
    },
    {
        "timestamp": "2026-06-22T10:25:11Z",
        "environment": "simulated-prod",
        "traceId": "TRACE-10049",
        "transactionId": "TXN-793",
        "service": "payment-service",
        "level": "INFO",
        "eventType": "APPLICATION_LOG",
        "errorCode": "NONE",
        "latencyMs": 260,
        "message": "Payment completed successfully"
    }
]

def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for log in logs:
            file.write(json.dumps(log) + "\n")

    print(f"Generated {len(logs)} logs")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()