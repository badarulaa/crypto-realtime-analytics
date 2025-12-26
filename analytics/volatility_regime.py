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
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
  )

  query = """
  SELECT price_usd, signal, vol_5
  FROM btc_analytics
  ORDER BY ts ASC
  """

  df = pd.read_sql_query(query, conn)
  conn.close()

  if df.empty:
    print("No Data")
    return

  threshold = df["vol_5"].median()

  df["vol_regime"] = df["vol_5"].apply(
    lambda x: "HIGH_VOL" if x >= threshold else "LOW_VOL"
  )

  summary = (
    df.groupby(["vol_regime","signal"])
    .size()
    .unstack(fill_value=0)
  )

  print("\n=== VOLATILITY REGIME SUMMARY ===")
  print(summary)

  print("\n=== PERCENTAGE BY REGIME ===")
  pct = summary.div(summary.sum(axis=1), axis=0) * 100
  print(pct.round(2))

if __name__ == "__main__":
  main()