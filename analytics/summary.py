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
  SELECT signal, vol_5, vol_10
  FROM btc_analytics
  """

  df = pd.read_sql(query, conn)
  conn.close()

  if df.empty:
    print("No Analytics data found.")
    return

  print("\n=== Signal Distribution ===")
  signal_counts = df["signal"].value_counts()
  print(signal_counts)

  print("\n=== Signal Percentage (%) ====")
  signal_pct = (signal_counts / len(df) * 100).round(2)
  print(signal_pct)

  print("\n=== Market Condition ===")
  market_conditions = (df["vol_5"] > df["vol_10"]).value_counts()
  market_conditions.index = ["Active Market", "Calm Market"]
  print(market_conditions)

  print("\n=== Interpretation ===")
  dominant_signal = signal_counts.idxmax()
  print(f"Most frequent signal: {dominant_signal}")

  if dominant_signal == "HOLD":
    print("Market mostly ranged / low momentum.")
  elif dominant_signal == "BUY":
    print("Bullish momentum.")
  else:
    print("Bearish momentum.")

if __name__ == "__main__":
  main()