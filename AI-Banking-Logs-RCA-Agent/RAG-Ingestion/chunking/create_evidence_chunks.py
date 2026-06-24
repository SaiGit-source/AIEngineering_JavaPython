import json
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_LOGS_FILE = BASE_DIR / "data" / "raw_logs.jsonl"
CHUNKS_FILE = BASE_DIR / "data" / "evidence_chunks.jsonl"

logs_by_trace_id = defaultdict(list)

with open(RAW_LOGS_FILE, "r", encoding="utf-8") as file:
    for line in file:
        log = json.loads(line)
        logs_by_trace_id[log["traceId"]].append(log)

with open(CHUNKS_FILE, "w", encoding="utf-8") as output_file:
    for trace_id, logs in logs_by_trace_id.items():
        logs = sorted(logs, key=lambda x: x["timestamp"])

        transaction_id = logs[0]["transactionId"]
        services = sorted(set(log["service"] for log in logs))
        error_codes = sorted(set(log["errorCode"] for log in logs if log["errorCode"] != "NONE"))

        text_lines = [
            f"Evidence logs for traceId {trace_id} and transactionId {transaction_id}.",
            "The following logs show the request flow in timestamp order:",
            ""
        ]

        for log in logs:
            text_lines.append(
                f"{log['timestamp']} | "
                f"service={log['service']} | "
                f"level={log['level']} | "
                f"eventType={log['eventType']} | "
                f"errorCode={log['errorCode']} | "
                f"latencyMs={log['latencyMs']} | "
                f"message={log['message']}"
            )

        chunk = {
            "id": f"trace-{trace_id}",
            "traceId": trace_id,
            "transactionId": transaction_id,
            "services": services,
            "errorCodes": error_codes,
            "environment": logs[0]["environment"],
            "text": "\n".join(text_lines)
        }

        output_file.write(json.dumps(chunk) + "\n")

print(f"Created {len(logs_by_trace_id)} evidence chunk(s)")
print(f"Saved to {CHUNKS_FILE}")