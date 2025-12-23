import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def init_tables():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    with conn:
        with conn.cursor() as cur:
            # raw price table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS btc_price (
                ts TIMESTAMPTZ PRIMARY KEY,
                price_usd NUMERIC,
                raw_json JSONB
            );
            """)

            # analytics table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS btc_analytics (
                ts TIMESTAMPTZ PRIMARY KEY,
                price_usd NUMERIC,
                sma_5 NUMERIC,
                sma_10 NUMERIC,
                vol_5 NUMERIC,
                vol_10 NUMERIC,
                signal TEXT,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """)

            # xau price table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS xau_price (
                ts TIMESTAMPTZ PRIMARY KEY,
                price_usd NUMERIC,
                raw_json JSONB
            );
            """)

    conn.close()
    print("Database tables are ready.")

if __name__ == "__main__":
    init_tables()
