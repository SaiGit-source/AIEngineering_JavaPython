# AI-Banking-Logs-RCA-Agent Project Summary

## 1. Project Overview

**AI-Banking-Logs-RCA-Agent** is an MVP production-support RCA system for simulated banking microservice logs.

The project demonstrates how AI can help a support engineer investigate banking application failures. It generates simulated logs, pushes them into AWS CloudWatch, processes them with AWS Lambda, stores trace-level evidence documents in Pinecone, and uses a Spring Boot backend with Spring AI to generate a root-cause analysis. A React dashboard shows operational charts and an AI RCA interaction panel.

The main idea is:

```text
Payment failures appear in logs
→ logs are grouped by traceId
→ relevant trace evidence is retrieved from Pinecone
→ AI explains root cause, symptom, impacted service, evidence, and suggested fix
```

---

## 2. High-Level Architecture

```text
React Dashboard
   ↓
Spring Boot Backend
   ↓
Pinecone Retrieval
   ↓
Spring AI ChatClient / OpenAI
   ↓
Structured RCA response shown in React
```

RAG ingestion flow:

```text
generate_logs.py
   ↓
data/raw_logs.jsonl
   ↓
watch_raw_logs_to_cloudwatch.py
   ↓
push_logs_to_cloudwatch.py
   ↓
AWS CloudWatch Logs
   ↓
CloudWatch Subscription Filter
   ↓
AWS Lambda
   ↓
Group logs by traceId
   ↓
Pinecone trace-level evidence documents
```

---

## 3. Main Components

## 3.1 Frontend: React Dashboard

The frontend is a **React + Vite** dashboard.

It has two main responsibilities:

1. Show operational dashboard charts from Spring Boot APIs.
2. Provide an AI RCA assistant panel where the user can ask production-support questions.

Current MVP frontend includes:

```text
3 charts
1 traces table
1 AI RCA panel
```

The MVP charts are:

```text
1. Error codes chart
2. Errors by service chart
3. Error trend chart
```

The frontend calls:

```text
GET  /api/dashboard/overview
POST /api/rca/analyze
```

Example user query for the AI panel:

```text
The dashboard shows repeated payment-service errors. Is payment-service the real root cause, or are upstream dependencies causing the failures?
```

---

## 3.2 Backend: Spring Boot + Spring AI

The backend is a **Spring Boot** application.

Backend responsibilities:

```text
1. Serve dashboard chart data to React
2. Retrieve relevant evidence documents from Pinecone
3. Send the user question and evidence to Spring AI ChatClient
4. Return structured RCA results to React
```

Important backend components:

```text
RcaController
DashboardController
RcaService
PineconeSearchService
DashboardService
```

### RcaController

Handles AI RCA APIs:

```text
POST /api/rca/search
POST /api/rca/analyze
```

### DashboardController

Handles dashboard data API:

```text
GET /api/dashboard/overview
```

This one API returns the data needed for the React charts and trace table:

```json
{
  "errorCodes": [],
  "errorsByService": [],
  "errorTrend": [],
  "traces": []
}
```

### RcaService

Coordinates the RAG flow:

```text
User question
→ Pinecone evidence retrieval
→ Spring AI ChatClient
→ structured RCA JSON
```

The returned RCA structure is:

```json
{
  "question": "...",
  "rootCause": "...",
  "symptom": "...",
  "impactedService": "...",
  "evidence": ["..."],
  "suggestedFix": ["..."],
  "retrievedEvidence": ["..."]
}
```

### PineconeSearchService

This service calls Pinecone using REST.

Because the Pinecone index uses **integrated embeddings**, Spring Boot does not manually generate embeddings. It sends the text query directly to Pinecone.

Current retrieval setting:

```properties
pinecone.top-k=2
```

So only 2 context documents are provided to the AI.

### DashboardService

This service reads:

```text
data/raw_logs.jsonl
```

and calculates:

```text
errorCodes
errorsByService
errorTrend
traces
```

For the MVP, dashboard charts come from the backend reading the raw log file, not directly from CloudWatch.

---

## 3.3 RAG Ingestion Layer

The ingestion layer creates the evidence documents used by AI.

It includes:

```text
generate_logs.py
watch_raw_logs_to_cloudwatch.py
push_logs_to_cloudwatch.py
AWS CloudWatch Logs
AWS Lambda
Pinecone
```

---

# 4. What is RAG?

RAG means **Retrieval-Augmented Generation**.

In a normal AI chat flow, the AI only uses the prompt and its trained knowledge. In this project, the AI first receives actual log evidence from Pinecone.

The RAG flow is:

```text
User question
→ retrieve relevant trace evidence from Pinecone
→ add evidence to the AI prompt
→ AI generates RCA using that evidence
```

This is useful because the AI is grounded in project logs instead of guessing.

Example:

```text
Question:
Why is payment-service failing?

Retrieved evidence:
TRACE-10045 shows fraud-service unhealthy and pod restart.
TRACE-10046 shows account-service DB connection errors.

AI answer:
payment-service is mainly the symptom. The likely root causes are upstream dependency failures.
```

---

# 5. How AI Helps Here

AI helps convert noisy technical logs into a clear production-support explanation.

Without AI, the engineer manually reads logs like:

```text
payment-service ERROR FRAUD_TIMEOUT
fraud-service ERROR SERVICE_UNHEALTHY
fraud-service WARN POD_RESTARTED
```

With AI, the system explains:

```text
Root Cause:
fraud-service became unhealthy and restarted after health check failures.

Symptom:
payment-service failed with FRAUD_TIMEOUT.

Impacted Service:
payment-service.

Evidence:
fraud-service readiness probe returned 503 and pod restarted.

Suggested Fix:
check fraud-service pod restart reason, readiness probe configuration, and resource usage.
```

AI is helpful because it:

```text
1. Summarizes noisy logs
2. Connects downstream symptoms to upstream root causes
3. Explains RCA in support-friendly language
4. Suggests next troubleshooting steps
5. Reduces manual trace investigation time
```

---

# 6. Different Flows in the Project

## 6.1 RAG Ingestion Flow

This flow prepares evidence for AI retrieval.

```text
generate_logs.py
   ↓
data/raw_logs.jsonl
   ↓
watch_raw_logs_to_cloudwatch.py
   ↓
push_logs_to_cloudwatch.py
   ↓
AWS CloudWatch Logs
   ↓
CloudWatch Subscription Filter
   ↓
AWS Lambda
   ↓
Group logs by traceId
   ↓
Pinecone
```

### generate_logs.py

Creates simulated banking microservice logs and writes them to:

```text
data/raw_logs.jsonl
```

Each line is one JSON log event with fields like:

```json
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
}
```

### watch_raw_logs_to_cloudwatch.py

Watches `data/raw_logs.jsonl`.

When the file changes, it automatically runs:

```text
cloud/push_logs_to_cloudwatch.py
```

### push_logs_to_cloudwatch.py

Pushes raw JSON logs into CloudWatch.

CloudWatch location:

```text
Log group:  /banking/simulated-prod
Log stream: local-log-generator
```

CloudWatch contains raw individual logs, not consolidated chunks.

### CloudWatch Subscription Filter

Forwards new CloudWatch log events to Lambda.

```text
CloudWatch Logs → Lambda
```

### Lambda Function

Lambda receives compressed CloudWatch batches.

It does:

```text
1. Decode CloudWatch payload
2. Parse JSON log messages
3. Group logs by traceId
4. Create one evidence document per traceId
5. Upsert records to Pinecone using REST API
```

Example:

```text
TRACE-10045 raw logs
→ one Pinecone document called trace-TRACE-10045
```

### Pinecone

Pinecone stores consolidated trace-level evidence documents.

```text
CloudWatch = raw logs
Pinecone = grouped trace-level evidence documents
```

---

## 6.2 Dashboard Flow

This flow powers the charts.

```text
React dashboard
   ↓
GET /api/dashboard/overview
   ↓
Spring Boot DashboardController
   ↓
DashboardService
   ↓
Read data/raw_logs.jsonl
   ↓
Calculate chart data
   ↓
Return JSON to React
```

Charts are deterministic and do not use AI.

Current chart data:

```text
errorCodes
errorsByService
errorTrend
traces
```

---

## 6.3 RCA Search Flow

This flow retrieves Pinecone evidence without generating an AI answer.

```text
React or Postman
   ↓
POST /api/rca/search
   ↓
Spring Boot RcaController
   ↓
RcaService
   ↓
PineconeSearchService
   ↓
Pinecone top 2 search results
   ↓
Evidence returned
```

This is useful for debugging what Pinecone returns.

---

## 6.4 AI RCA Flow

This is the main RAG flow.

```text
React AI panel
   ↓
POST /api/rca/analyze
   ↓
Spring Boot RcaController
   ↓
RcaService
   ↓
PineconeSearchService retrieves top 2 evidence documents
   ↓
Spring AI ChatClient sends question + evidence to OpenAI
   ↓
AI returns structured RCA JSON
   ↓
React displays RCA cards
```

The AI is asked to return:

```text
Root Cause
Symptom
Impacted Service
Evidence
Suggested Fix
```

---

# 7. Frontend Breakdown

Frontend files:

```text
src/App.jsx
src/api.js
src/components/KpiCards.jsx
src/components/ChartsSection.jsx
src/components/TraceTable.jsx
src/components/AiRcaPanel.jsx
src/components/Card.jsx
src/styles.css
```

## App.jsx

Main layout. It loads dashboard data from:

```text
GET /api/dashboard/overview
```

and renders:

```text
KPI cards
3 charts
trace table
AI RCA panel
```

## api.js

Central API file.

Calls:

```text
GET  /api/dashboard/overview
POST /api/rca/analyze
```

## KpiCards.jsx

Shows summary metrics:

```text
Total error signals
Impacted services
Affected traces
Environment
```

## ChartsSection.jsx

Shows 3 Recharts charts:

```text
Error codes
Errors by service
Error trend
```

## TraceTable.jsx

Shows traces returned by backend. Selecting a trace updates the AI question.

## AiRcaPanel.jsx

Lets the user ask an RCA question. It calls:

```text
POST /api/rca/analyze
```

and displays:

```text
Root cause
Impacted service
Symptom
Evidence
Suggested fix
Retrieved Pinecone evidence
```

---

# 8. Backend Breakdown

Main packages:

```text
com.banking.rca_backend.controller
com.banking.rca_backend.service
com.banking.rca_backend.dto
```

## Controllers

```text
RcaController
DashboardController
```

### RcaController

Handles:

```text
POST /api/rca/search
POST /api/rca/analyze
```

### DashboardController

Handles:

```text
GET /api/dashboard/overview
```

## Services

```text
RcaService
PineconeSearchService
DashboardService
```

### RcaService

Coordinates:

```text
question
→ Pinecone evidence
→ ChatClient
→ structured RCA
```

### PineconeSearchService

Calls Pinecone REST search.

Uses:

```text
PINECONE_API_KEY
PINECONE_INDEX_HOST
PINECONE_NAMESPACE
pinecone.top-k=2
```

### DashboardService

Reads raw logs and creates dashboard data.

Uses:

```text
dashboard.logs-file
```

---

# 9. Environment Variables and Properties

## .env

```env
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_HOST=your_pinecone_index_host
PINECONE_NAMESPACE=simulated-prod
```

## application.properties

```properties
spring.config.import=optional:file:.env[.properties]

spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.model.chat=openai
spring.ai.model.audio.speech=none
spring.ai.model.audio.transcription=none
spring.ai.model.embedding=none
spring.ai.model.image=none
spring.ai.model.moderation=none

pinecone.api-key=${PINECONE_API_KEY}
pinecone.index-host=${PINECONE_INDEX_HOST}
pinecone.namespace=${PINECONE_NAMESPACE:simulated-prod}
pinecone.api-version=2025-10
pinecone.top-k=2

dashboard.logs-file=C:/Users/saito/source/repos/AIEngineering_JavaPython/AI-Banking-Logs-RCA-Agent/data/raw_logs.jsonl
```

---

# 10. Important Design Decisions

## CloudWatch stores raw logs

CloudWatch contains individual log entries:

```text
payment-service ERROR FRAUD_TIMEOUT
fraud-service ERROR SERVICE_UNHEALTHY
fraud-service WARN POD_RESTARTED
```

## Lambda groups by traceId

Lambda groups raw logs by `traceId` and creates one consolidated evidence document per trace.

Example:

```text
TRACE-10045
→ auth-service log
→ account-service log
→ payment-service FRAUD_TIMEOUT
→ fraud-service SERVICE_UNHEALTHY
→ fraud-service POD_RESTARTED
```

becomes:

```text
trace-TRACE-10045
```

in Pinecone.

## Pinecone stores RAG evidence

Pinecone is used for semantic retrieval. It stores trace-level documents and returns relevant evidence for the user question.

## Spring AI generates the RCA

Spring AI ChatClient receives:

```text
user question
+ top 2 Pinecone evidence documents
```

and returns structured RCA.

## Dashboard charts do not use AI

Charts are calculated from raw logs.

```text
Charts = deterministic aggregation
AI RCA = evidence-based explanation
```

---

# 11. Example Demo Scenario

Dashboard shows repeated errors in:

```text
payment-service
```

User asks:

```text
The dashboard shows repeated payment-service errors. Is payment-service the real root cause, or are upstream dependencies causing the failures?
```

Pinecone retrieves evidence such as:

```text
TRACE-10045: fraud-service unhealthy caused payment-service FRAUD_TIMEOUT
TRACE-10046: account-service DB issue caused payment-service BALANCE_CHECK_FAILED
```

AI explains:

```text
payment-service is mainly the downstream symptom.
The root causes are upstream dependency failures:
1. fraud-service was unhealthy and restarted
2. account-service had DB connection issues
```

This is the main value of the project.

---

# 12. How to Run

## Generate logs

```powershell
python log-generator\generate_logs.py
```

## Start watcher

```powershell
python automation\watch_raw_logs_to_cloudwatch.py
```

## Start Spring Boot

Run the backend from IntelliJ or Maven.

Backend URL:

```text
http://localhost:8080
```

## Test dashboard API

```text
GET http://localhost:8080/api/dashboard/overview
```

## Test RCA API

```text
POST http://localhost:8080/api/rca/analyze
```

Body:

```json
{
  "question": "The dashboard shows repeated payment-service errors. Is payment-service the real root cause, or are upstream dependencies causing the failures?"
}
```

## Start React

```powershell
cd rca-dashboard-final
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 13. MVP Status

Completed:

```text
Simulated banking logs
CloudWatch ingestion
Lambda processing
Pinecone upsert
Spring Boot Pinecone retrieval
Spring AI ChatClient RCA
React dashboard MVP
3 backend-driven charts
Trace table
AI interaction panel
```

Not included in MVP:

```text
Real EKS deployment
Real Kubernetes logs
Real CloudWatch Logs Insights chart queries
Database persistence
User authentication
Production-grade trace window aggregation
```

These can be added later.
