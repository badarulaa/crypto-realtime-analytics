# Crypto Realtime Analytics Pipeline (BTC)

End-to-end crypto analytics pipeline built with Python and PostgreSQL.

This project fetches real-time Bitcoin price data, performs technical analysis
(Simple Moving Average, Volatility), generates trading signals (BUY / SELL / HOLD),
and stores both raw and analytics data into a database.

## Features
- Realtime BTC price ingestion (loop-based)
- PostgreSQL as data storage
- Technical indicators:
  - SMA 5 / SMA 10
  - Rolling volatility
- Rule-based signal generation
- Automated analytics loop
- Visualization (price, SMA, signals)

## Tech Stack
- Python
- PostgreSQL
- pandas
- psycopg2
- matplotlib

## How It Works
1. Ingestion loop fetches BTC price every 5 minutes
2. Raw data stored in `btc_price`
3. Analytics computes indicators and signals
4. Results stored in `btc_analytics`
5. Visualization reads from analytics table

## Acknowledgements
This project was developed with guidance and mentorship from **ChatGPT (OpenAI)**,
acting as a technical mentor throughout the design and implementation of the
data pipeline, analytics logic, automation, and visualization.

The human author made all final decisions, implementations, and validations.

## Disclaimer
This project is for educational and analytical purposes only.
It is **not** financial or trading advice.
