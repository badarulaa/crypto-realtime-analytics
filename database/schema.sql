-- database/schema.sql

CREATE DATABASE crypto_db;

-- (jalankan sebagai superuser -> CREATE USER & GRANT)
-- contoh commands (di shell):
-- psql -U postgres -c "CREATE USER crypto_user WITH PASSWORD 'strongpassword';"
-- psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE crypto_db TO crypto_user;"

-- setelah membuat DB, jalankan di dalam crypto_db:
CREATE TABLE IF NOT EXISTS btc_price (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    price_usd NUMERIC(18,8) NOT NULL,
    raw_json JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_btc_price_ts ON btc_price (ts);
