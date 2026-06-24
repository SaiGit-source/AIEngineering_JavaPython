# Banking RCA Dashboard MVP

React + Vite frontend for the AI-Banking-Logs-RCA-Agent project.

This version does **not** use mock data.

## Backend required

Run Spring Boot on:

```text
http://localhost:8080
```

Required APIs:

```text
GET  /api/dashboard/overview
POST /api/rca/analyze
```

## Expected dashboard API response

```json
{
  "errorCodes": [
    { "errorCode": "FRAUD_TIMEOUT", "count": 1 }
  ],
  "errorsByService": [
    { "service": "payment-service", "errors": 2 }
  ],
  "errorTrend": [
    { "time": "10:15:31", "errors": 1 }
  ],
  "traces": [
    {
      "traceId": "TRACE-10045",
      "transactionId": "TXN-789",
      "services": "payment-service, fraud-service",
      "errorCodes": "FRAUD_TIMEOUT, SERVICE_UNHEALTHY",
      "severity": "High"
    }
  ]
}
```

## Expected RCA API response

```json
{
  "question": "Why did TRACE-10045 fail?",
  "rootCause": "...",
  "symptom": "...",
  "impactedService": "...",
  "evidence": ["..."],
  "suggestedFix": ["..."],
  "retrievedEvidence": ["..."]
}
```

## Run

```bash
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```
