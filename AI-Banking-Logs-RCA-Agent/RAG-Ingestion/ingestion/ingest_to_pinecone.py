import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_FILE = BASE_DIR / "data" / "evidence_chunks.jsonl"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "banking-logs-rca")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "simulated-prod")

if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY in .env")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

records = []

with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    for line in file:
        chunk = json.loads(line)

        record = {
            "_id": chunk["id"],
            "text": chunk["text"],
            "traceId": chunk["traceId"],
            "transactionId": chunk["transactionId"],
            "services": ",".join(chunk["services"]),
            "errorCodes": ",".join(chunk["errorCodes"]),
            "environment": chunk["environment"]
        }
        
        records.append(record)

response = index.upsert_records(
    namespace=PINECONE_NAMESPACE,
    records=records
)

print(f"Submitted {len(records)} records to Pinecone")
print(response)