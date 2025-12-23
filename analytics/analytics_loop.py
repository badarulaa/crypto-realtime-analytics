import time
from datetime import datetime
import sys
from pathlib import Path

# Setup root project
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from analytics.run_analytics import main as run_analytics

INTERVAL_SECONDS = 300

def log(msg: str):
  ts = datetime.utcnow().isoformat()
  print(f"[{ts}] {msg}", flush=True)

if __name__ == "__main__":
  log("Analytics loop STARTED")

  while True:
    try:
      log("Running analytics...")
      run_analytics()
      log("Analytics run complete. Sleep 5 minutes...")
    except Exception as e:
      log(f"ERROR during analytics: {repr(e)}")

    time.sleep(INTERVAL_SECONDS)