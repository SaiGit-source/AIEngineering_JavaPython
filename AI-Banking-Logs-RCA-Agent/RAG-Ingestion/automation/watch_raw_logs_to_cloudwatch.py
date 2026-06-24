import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_LOGS_FILE = BASE_DIR / "data" / "raw_logs.jsonl"
PUSH_SCRIPT = BASE_DIR / "cloud" / "push_logs_to_cloudwatch.py"


class RawLogsChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run_time = 0

    def on_modified(self, event):
        changed_file = Path(event.src_path)

        if changed_file.resolve() != RAW_LOGS_FILE.resolve():
            return

        now = time.time()

        # Prevent duplicate triggers from one file save
        if now - self.last_run_time < 2:
            return

        self.last_run_time = now

        print("raw_logs.jsonl changed")
        print("Pushing logs to CloudWatch...")

        result = subprocess.run(
            [sys.executable, str(PUSH_SCRIPT)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.stderr:
            print("ERROR:")
            print(result.stderr)


def main():
    if not RAW_LOGS_FILE.exists():
        print(f"File not found: {RAW_LOGS_FILE}")
        return

    print("Watching raw logs file:")
    print(RAW_LOGS_FILE)
    print("Press Ctrl+C to stop.")

    observer = Observer()
    observer.schedule(
        RawLogsChangeHandler(),
        path=str(RAW_LOGS_FILE.parent),
        recursive=False
    )

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()