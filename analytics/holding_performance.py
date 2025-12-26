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
  FROM btc_analytics
  ORDER BY ts ASC;
  """

  df = pd.read_sql_query(query, conn)
  conn.close()

  if df.empty or len(df) < 6:
    print("Not enough data for performance evaluation")
    return

  results = {}

  for horizon in [1, 2, 3, 4, 5]:
    df[f"future_price_{horizon}"] = df["price_usd"].shift(-horizon)

    cond_sell = (df["signal"] == "BUY") & (
      df[f"future_price{horizon}"] > df["price_usd"]
    )

    cond_buy = (df["signal"] == "SELL") & (
      df[f"future_price{horizon}"] < df["price_usd"]
    )

    valid = df["signal"].isin(["BUY", "SELL"])

    correct = (cond_buy | cond_sell) & valid
    accuracy = correct.sum() / valid.sum() * 100

    results[horizon] = round(accuracy, 2)

  print("\n=== HOLDING PERIOD PERFORMANCE ===")
  for k, v in results.items():
    print(f"Horizon {k}: accuracy = {v}%")

if __name__ == "__main__":
  main()
