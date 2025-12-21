import os
from datetime import datetime
from pathlib import Path
import requests
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

API_URL = os.getenv("API_URL")
DATA_DIR = Path(os.getenv("DATA_DIR", "./data/raw"))

DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = DATA_DIR/"btc_raw.csv"

def main():
  #1. Fetch BTC Price
  response = requests.get(API_URL, timeout=10)
  response.raise_for_status()
  data = response.json()

  price = float(data["bitcoin"]["usd"])
  ts = datetime.utcnow().isoformat()

  #2. Save to CSV
  if not CSV_FILE.exists():
    CSV_FILE.write_text("timestamp,price_usd\n")

  with CSV_FILE.open("a") as f:
    f.write(f"{ts},{price}\n")

  #3. Insert into DB
  conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
  )

  with conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        INSERT INTO btc_price (ts, price_usd, raw_json)
        VALUES (%s, %s, %s)
        """,
        (ts, price, Json(data))
      )

  conn.close()
  print(f"BTC Price inserted: {price} USD at {ts}")

if __name__ == "__main__":
  main()