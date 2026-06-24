import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "banking-logs-rca")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "simulated-prod")

if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY in .env")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

question = "Which trace shows fraud-service causing payment failure?"

results = index.search(
    namespace=PINECONE_NAMESPACE,
    query={
        "inputs": {
            "text": question
        },
        "top_k": 3
    },
    fields=[
        "text",
        "traceId",
        "transactionId",
        "services",
        "errorCodes",
        "environment"
    ]
)

# Convert result object to dictionary if needed
if hasattr(results, "to_dict"):
    results = results.to_dict()

hits = results.get("result", {}).get("hits", [])

print("\nQuestion:")
print(question)

print("\nPinecone Search Results:")

if not hits:
    print("No results found.")
    print("Try running: python ingestion/ingest_to_pinecone.py")
else:
    for hit in hits:
        print("\n---------------------------")
        print("Score:", hit.get("_score"))
        print("ID:", hit.get("_id"))

        fields = hit.get("fields", {})

        print("Trace ID:", fields.get("traceId"))
        print("Transaction ID:", fields.get("transactionId"))
        print("Services:", fields.get("services"))
        print("Error Codes:", fields.get("errorCodes"))
        print("Environment:", fields.get("environment"))

        print("\nEvidence Text:")
        print(fields.get("text"))