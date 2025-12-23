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
    SELECT ts, price_usd, signal
    FROM btc_analytics
    ORDER BY ts ASC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty or len(df) < 2:
        print("Not enough data for performance evaluation")
        return

    # shift price to get next-period price
    df["next_price"] = df["price_usd"].shift(-1)
    df = df.dropna()

    # evaluate signals
    df["signal_result"] = "NEUTRAL"

    df.loc[
        (df["signal"] == "BUY") & (df["next_price"] > df["price_usd"]),
        "signal_result"
    ] = "CORRECT"

    df.loc[
        (df["signal"] == "BUY") & (df["next_price"] <= df["price_usd"]),
        "signal_result"
    ] = "WRONG"

    df.loc[
        (df["signal"] == "SELL") & (df["next_price"] < df["price_usd"]),
        "signal_result"
    ] = "CORRECT"

    df.loc[
        (df["signal"] == "SELL") & (df["next_price"] >= df["price_usd"]),
        "signal_result"
    ] = "WRONG"

    performance = df[df["signal"].isin(["BUY", "SELL"])]

    print("\n=== SIGNAL PERFORMANCE ===")
    print(performance["signal_result"].value_counts())

    if not performance.empty:
        accuracy = (
            (performance["signal_result"] == "CORRECT").mean() * 100
        ).round(2)
        print(f"\nSignal accuracy: {accuracy}%")

    print("\n=== SAMPLE EVALUATION ===")
    print(
        performance[
            ["ts", "signal", "price_usd", "next_price", "signal_result"]
        ].tail(10)
    )


if __name__ == "__main__":
    main()
