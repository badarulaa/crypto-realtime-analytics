import time
from fetch_btc_once import main

INTERVAL = 300

if __name__ == "__main__":
  while True:
    try:
      main()
    except Exception as e:
      print("Error", e)
    time.sleep(INTERVAL)