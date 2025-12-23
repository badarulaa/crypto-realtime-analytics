import os
from datetime import timezone
import yfinance as yf
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SYMBOL = "GC=F"  # Gold Futures


def main():
    print("Fetching XAUUSD historical data from Yahoo Finance...")

    df = yf.download(
        SYMBOL,
        period="2y",     # 2 years data
        interval="1d",   # daily
        progress=False
    )

    if df.empty:
        print("No data returned from Yahoo Finance")
        return

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    inserted = 0

    with conn:
        with conn.cursor() as cur:
            for ts, row in df.iterrows():
                price = float(row["Close"])
                ts = ts.tz_localize(timezone.utc)

                raw = {
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": price,
                    "volume": int(row["Volume"]) if not row["Volume"] != row["Volume"] else None
                }

                cur.execute(
                    """
                    INSERT INTO xau_price (ts, price_usd, raw_json)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (ts) DO NOTHING
                    """,
                    (ts, price, Json(raw))
                )
                inserted += 1

    conn.close()
    print(f"Inserted {inserted} rows into xau_price")


if __name__ == "__main__":
    main()
