import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def main():
  conn =psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
  )

  query = """
  SELECT ts, price_usd, sma_5, sma_10, signal
  FROM btc_analytics
  ORDER BY ts ASC
  """

  df = pd.read_sql(query, conn, parse_dates=["ts"])
  conn.close()

  if df.empty():
    print("No analytics data found.")
    return

  # Plot
  plt.figure(figsize=(14, 7))
  plt.plot(df["ts"], df["price_usd"], label="BTC Price")
  plt.plot(df["ts"], df["sma_5"], label="SMA 5")
  plt.plot(df["ts"], df["sma_10"], label="SMA 10")

  # Plot Buy/Sell signals
  buy_signals = df[df["signal"] == "BUY"]
  sell_signals = df[df["signal"] == "SELL"]

  plt.scatter(
    buy_signals["ts"],
    buy_signals["price_usd"],
    marker="^",
    s=100,
    label="BUY"
  )

  plt.scatter(
    sell_signals["ts"],
    sell_signals["price_usd"],
    marker="v",
    s=100,
    label="SELL"
  )

  plt.title("BTC Price with SMA & Trading Signals")
  plt.xlabel("Time")
  plt.ylabel("Price (USD)")
  plt.legend()
  plt.grid(True)

  plt.show()

if __name__ == "__main__":
  main()
