import time
import sys
from pathlib import Path
from datetime import datetime, timezone

# Tambahkan root project ke PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ingestion.fetch_btc_once import main as fetch_once


INTERVAL_SECONDS = 300  # 5 menit


def log(msg):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] {msg}", flush=True)


if __name__ == "__main__":
    log("BTC ingestion loop STARTED")

    while True:
        try:
            log("Running fetch_btc_once...")
            fetch_once()
            log("Sleep 5 minutes...")
        except Exception as e:
            log(f"ERROR: {repr(e)}")

        time.sleep(INTERVAL_SECONDS)
