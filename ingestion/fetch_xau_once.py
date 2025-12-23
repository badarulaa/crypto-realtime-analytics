import os
from datetime import datetime, timezone
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

API_URL = "https://api.exchangerate.host/latest?base=XAU&symbols=USD"

def main():
  response = requests.get(API_URL, timeout=10)
  response.raise_for_status()
  data = response.json()

  price = float(data["rates"["USD"]])
  ts = datetime.now(timezone.utc).isoformat()

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
        INSERT INTO xau_price (ts, price_usd, raw_json)
        VALUES (%s, %s, %s)
        """,
        (ts, price, Json(data))
      )

  conn.close()
  print(f"[XAUUSD] inserted {price} at {ts}")

if __name__ == "__main__":
  main()