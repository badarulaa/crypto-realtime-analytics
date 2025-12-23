import os
from datetime import datetime, timezone
import requests
import psycopg2
import csv
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

API_URL = "https://stooq.com/q/l/?s=xauusd&i=5"

def main():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    csv_text = response.text
    reader = csv.DictReader(StringIO(csv_text))
    rows = list(reader)

    # 🔒 SAFETY CHECK
    if not rows:
        print("[XAUUSD] No data returned from Stooq (market closed or no update)")
        return

    row = rows[0]

    price = float(row["Close"])
    date_str = f"{row['Date']} {row['Time']}"
    ts = datetime.strptime(
        date_str, "%Y-%m-%d %H:%M"
    ).replace(tzinfo=timezone.utc)

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
                (ts, price, row)
            )

    conn.close()
    print(f"[XAUUSD] inserted {price} at {ts}")

if __name__ == "__main__":
    main()
