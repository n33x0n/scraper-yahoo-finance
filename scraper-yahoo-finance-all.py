# Yahoo Finance Scraper v.1.3
# Autor: Tomasz Lebioda
# Email: tlebioda@gmail.com

import yfinance as yf
from yfinance.exceptions import YFRateLimitError
import pandas as pd
from datetime import datetime
import pytz
import time
import random
import os

# Backoff configuration
MAX_RETRIES = 5
BASE_WAIT = 60
PER_TICKER_MIN = 1
PER_TICKER_MAX = 5

def fetch_with_backoff(symbol, start, end):
    wait = BASE_WAIT
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            df = yf.Ticker(symbol).history(start=start, end=end)
            # Throttle even on success to avoid bursts
            time.sleep(random.uniform(PER_TICKER_MIN, PER_TICKER_MAX))
            return df
        except YFRateLimitError:
            print(f"[{symbol}] Rate limited (attempt {attempt}/{MAX_RETRIES}). Sleeping {wait}s…")
            jitter = wait * 0.2
            time.sleep(wait + random.uniform(-jitter, jitter))
            wait *= 2
    print(f"[{symbol}] FAILED after {MAX_RETRIES} retries – skipping.")
    return pd.DataFrame(columns=["Close"])

# Konfiguracja tickerów: symbol -> (nazwa kolumny, liczba miejsc po przecinku)
TICKER_CONFIG = {
    "^GDAXI":   ("DAX", 2),
    "000001.SS":("China Shanghai SE Composite", 2),
    "^FTSE":    ("the UK FTSE 100", 2),
    "^GSPTSE":  ("Canada S&P/TSX Composite", 2),
    "^GSPC":    ("The US S&P 500", 2),
    "^N225":    ("Japan Nikkei 225", 2),
    "BTC-USD":  ("Bitcoin", 4),
    "ETH-USD":  ("Ethereum", 4),
    "XRP-USD":  ("XRP", 4),
    "SOL-USD":  ("Solana", 4),
    "DOGE-USD": ("DOGE", 4),
    "USDT-USD": ("USDT", 4),
    "TSLA":     ("Tesla", 2),
    "SPAX.PVT": ("SPAX.PVT", 2),
    "PLN=X":    ("USD/PLN", 4),
    "EURPLN=X": ("EUR/PLN", 4),
    "AMZN":     ("Amazon", 2),
    "GBPPLN=X": ("GBP/PLN", 4),
    "WIG20.WA": ("WIG20", 2)
}

START_DATE = "2025-01-01"
OUTPUT_FILE = "scraped-data.csv"

def get_today_date():
    warsaw = pytz.timezone("Europe/Warsaw")
    return datetime.now(warsaw).strftime("%Y-%m-%d")

# 1) Wczytaj dotychczasowe dane, jeśli plik istnieje
if os.path.exists(OUTPUT_FILE):
    df_existing = pd.read_csv(OUTPUT_FILE, parse_dates=["date"], index_col="date")
else:
    df_existing = None

# 2) Przygotuj pełen zakres dat od START_DATE do dziś
end_date = get_today_date()
all_dates = pd.date_range(start=START_DATE, end=end_date, freq='D', tz=None)
result_df = pd.DataFrame(index=all_dates)

print("Yahoo Finance Scraper: 🚀 Gathering data from Yahoo Finance...\n")

# 3) Dla każdego tickera pobierz historię i połącz z dotychczasowymi danymi
for symbol, (col_name, decimals) in TICKER_CONFIG.items():
    print(f"Yahoo Finance Scraper: ⏳ Downloading {col_name} ({symbol})...", end=" ")
    # Pobierz historyczne Close z backoff retry
    hist = fetch_with_backoff(symbol, START_DATE, end_date)
    if not hist.empty:
        print("✅")
    else:
        print("⚠️ (skipped/empty)")

    # Usuń strefę czasową, jeśli mamy DatetimeIndex
    if isinstance(hist.index, pd.DatetimeIndex):
        hist.index = hist.index.tz_localize(None)

    # Przygotuj serię z historią
    if not hist.empty:
        series_new = hist["Close"].rename(col_name).round(decimals)
    else:
        series_new = pd.Series(name=col_name, dtype=float)

    # Zreindexuj do pełnego zakresu dat
    series_new = series_new.reindex(all_dates)

    # Jeśli były poprzednie dane, połącz: nowe nadpisują, stare zachowane
    if df_existing is not None and col_name in df_existing.columns:
        series_existing = df_existing[col_name].reindex(all_dates)
        combined = series_new.combine_first(series_existing)
    else:
        combined = series_new

    # Dodaj do wynikowego DF
    result_df[col_name] = combined

# 4) Zapisz wynik do CSV
result_df = result_df.reset_index().rename(columns={"index": "date"})
result_df["date"] = result_df["date"].dt.strftime("%Y-%m-%d")
result_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nYahoo Finance Scraper: 🎉 Done. Written to {OUTPUT_FILE} from {START_DATE} to {end_date} 📈")
