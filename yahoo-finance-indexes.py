import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import os

# Mapa indeksów: symbol Yahoo Finance -> nazwa w CSV
INDEX_MAP = {
    "^GDAXI": "DAX",
    "000001.SS": "China Shanghai SE Composite",
    "^FTSE": "the UK FTSE 100",
    "^GSPTSE": "Canada S&P/TSX Composite",
    "^GSPC": "The US S&P 500",
    "^N225": "Japan Nikkei 225"
}

# Ścieżka do pliku CSV
CSV_FILE = "index_data.csv"

# Aktualna data w strefie Europe/Warsaw
def get_today_date():
    warsaw = pytz.timezone("Europe/Warsaw")
    return datetime.now(warsaw).strftime("%Y-%m-%d")

def fetch_close_prices():
    data = {"date": get_today_date()}
    for symbol, name in INDEX_MAP.items():
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        if not hist.empty:
            close_value = hist["Close"].iloc[-1]
            data[name] = round(close_value, 2)
        else:
            data[name] = None
    return data

def append_to_csv_if_new(data):
    df_new = pd.DataFrame([data])

    if not os.path.exists(CSV_FILE):
        df_new.to_csv(CSV_FILE, index=False)
        return

    df_existing = pd.read_csv(CSV_FILE)

    if data["date"] in df_existing["date"].values:
        print("Dane dla tej daty już istnieją. Pomijam.")
        return

    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(CSV_FILE, index=False)

if __name__ == "__main__":
    prices = fetch_close_prices()
    append_to_csv_if_new(prices) 