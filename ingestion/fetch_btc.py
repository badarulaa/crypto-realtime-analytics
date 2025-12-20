# ingestion/fetch_btc.py
import os
import time
import json
from pathlib import Path
from datetime import datetime
import requests
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()  # loads .env from current working dir

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "crypto_db")
DB_USER = os.getenv("DB_USER", "crypto_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

API_URL = os.getenv("API_URL", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
DATA_DIR = Path(os.getenv("DATA_DIR", "./data/raw"))
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL_SECONDS", 300))

DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = DATA_DIR / "btc_raw.csv"

def fetch_price():
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()

def save_csv(timestamp_iso, price, raw_json):
    header = "timestamp_iso,price_usd,raw_json\n"
    line = f'"{timestamp_iso}",{price},"{json.dumps(raw_json).replace("\"","\'")}"\n'
    if not CSV_FILE.exists():
        CSV_FILE.write_text(header)
    CSV_FILE.write_text(line, append=True)

def insert_db(conn, timestamp_iso, price, raw_json):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO btc_price (ts, price_usd, raw_json)
            VALUES (%s, %s, %s)
            """,
            (timestamp_iso, price, Json(raw_json))
        )
    conn.commit()

def main_loop():
    # create DB connection
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    try:
        while True:
            try:
                data = fetch_price()
                # expected structure: {"bitcoin":{"usd": 12345.67}}
                price = None
                if "bitcoin" in data and "usd" in data["bitcoin"]:
                    price = float(data["bitcoin"]["usd"])
                timestamp_iso = datetime.utcnow().isoformat()

                # save raw CSV (raw_json saved as string)
                save_csv(timestamp_iso, price, data)

                # insert to DB
                insert_db(conn, timestamp_iso, price, data)

                print(f"[{timestamp_iso}] saved price: {price} USD")
            except Exception as e:
                # log error, don't crash; wait and retry next cycle
                print(f"[{datetime.utcnow().isoformat()}] ERROR: {e}")

            time.sleep(FETCH_INTERVAL)
    finally:
        conn.close()

if __name__ == "__main__":
    main_loop()
