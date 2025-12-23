import os
import sys
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Setup path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from analytics.moving_average import simple_moving_average
from analytics.volatility import volatility

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def main():
  conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
  )

  query = """
  SELECT ts, price_usd
  FROM btc_price
  ORDER BY ts ASC
  """

  df = pd.read_sql_query(query, conn)
  conn.close()

  if df.empty:
    print("No data found")
    return

  df["sma_5"] = simple_moving_average(df["price_usd"], window=5)
  df["sma_10"] = simple_moving_average(df["price_usd"], window=10)
  df["vol_5"] = volatility(df["price_usd"], window=5)
  df["vol_10"] = volatility(df["price_usd"], window=10)

  print(df.tail(10))

if __name__ == "__main__":
  main()