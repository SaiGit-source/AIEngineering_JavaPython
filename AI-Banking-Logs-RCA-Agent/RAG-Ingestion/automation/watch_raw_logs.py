import subprocess
import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_LOGS_FILE = BASE_DIR / "data" / "raw_logs.jsonl"

class RawLogChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run_time = 0

    def on_modified(self, event):
        changed_file = Path(event.src_path)

        if changed_file != RAW_LOGS_FILE:
            return

        current_time = time.time()
        if current_time - self.last_run_time < 2:
            return

        self.last_run_time = current_time

        print("New raw log detected. Creating chunks...")

        subprocess.run(
            [sys.executable, "chunking/create_evidence_chunks.py"],
            cwd=BASE_DIR,
            check=True
        )

        print("Ingesting chunks into Pinecone...")

        subprocess.run(
            [sys.executable, "ingestion/ingest_to_pinecone.py"],
            cwd=BASE_DIR,
            check=True
        )

        print("Pinecone updated successfully.")


if __name__ == "__main__":
    print(f"Using Python: {sys.executable}")
    print(f"Watching file: {RAW_LOGS_FILE}")

    event_handler = RawLogChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(RAW_LOGS_FILE.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()