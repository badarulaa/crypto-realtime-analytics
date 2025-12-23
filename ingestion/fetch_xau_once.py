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

API_URL = "https://api.metals.live/v1/spot/gold"

def main():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    # metals.live returns a list
    record = data[0]
    price = float(record["gold"])
    ts = datetime.fromtimestamp(record["timestamp"], tz=timezone.utc)

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
                ON CONFLICT (ts) DO NOTHING
                """,
                (ts, price, Json(record))
            )

    conn.close()
    print(f"[XAUUSD] inserted {price} at {ts}")

if __name__ == "__main__":
    main()
