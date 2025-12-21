import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def main():
  conn = psycopg2.connect(
    host = DB_HOST,
    port = DB_PORT,
    dbname = DB_NAME,
    user = DB_USER,
    password = DB_PASSWORD
  )

  query = """
  SELECT ts, price_usd
  FROM btc_price
  ORDER BY ts ASC
  """

  df = pd.read_sql(query, conn)
  conn.close()

  if df.empty:
    print("No data found")
    return

  #hitung moving average
  df["ma_5"] = df["price_usd"].rolling(window=5).mean()
  df["ma_10"] = df["price_usd"].rolling(window=10).mean()

if __name__ == "__main__":
  main()