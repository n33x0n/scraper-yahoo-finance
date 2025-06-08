# Yahoo Finance Scraper v.1.5.0
# Copyright (C) 2025 Tomasz Lebioda <tlebioda@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: Tomasz Lebioda
# Email: tlebioda@gmail.com

import yfinance as yf
from yfinance.exceptions import YFRateLimitError
import pandas as pd
from datetime import datetime
import pytz
import time
import random
import os
import subprocess
import json
from pathlib import Path

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

# Ticker configuration: symbol -> (column name, decimal places)
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
REPORT_DIR = "reports"
EMAIL_TO = "tomasz.lebioda@wyborcza.pl"

def get_today_date():
    warsaw = pytz.timezone("Europe/Warsaw")
    return datetime.now(warsaw).strftime("%Y-%m-%d")

def get_current_datetime():
    warsaw = pytz.timezone("Europe/Warsaw")
    return datetime.now(warsaw).strftime("%Y-%m-%d %H:%M:%S")

class ReportGenerator:
    def __init__(self):
        self.report_data = {
            "timestamp": get_current_datetime(),
            "date": get_today_date(),
            "start_date": START_DATE,
            "tickers": {},
            "summary": {
                "total_tickers": 0,
                "successful": 0,
                "failed": 0,
                "total_records": 0,
                "missing_values": 0
            },
            "errors": []
        }
    
    def add_ticker_result(self, symbol, col_name, success, records=0, missing=0, error=None):
        self.report_data["tickers"][symbol] = {
            "name": col_name,
            "success": success,
            "records": records,
            "missing_values": missing,
            "error": str(error) if error else None
        }
        
        self.report_data["summary"]["total_tickers"] += 1
        if success:
            self.report_data["summary"]["successful"] += 1
            self.report_data["summary"]["total_records"] += records
            self.report_data["summary"]["missing_values"] += missing
        else:
            self.report_data["summary"]["failed"] += 1
            if error:
                self.report_data["errors"].append(f"{symbol}: {str(error)}")
    
    def generate_html_report(self):
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yahoo Finance Scraper Report - {self.report_data['date']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background-color: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .failed {{ color: #dc3545; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #007bff; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .error {{ background-color: #fee; padding: 10px; border-radius: 5px; margin: 5px 0; }}
        .footer {{ margin-top: 40px; text-align: center; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Yahoo Finance Scraper Report</h1>
        <p><strong>Execution time:</strong> {self.report_data['timestamp']}</p>
        <p><strong>Data range:</strong> {self.report_data['start_date']} - {self.report_data['date']}</p>
        
        <div class="summary">
            <h2>📈 Summary</h2>
            <p>Total tickers: <strong>{self.report_data['summary']['total_tickers']}</strong></p>
            <p>Successfully downloaded: <span class="success">{self.report_data['summary']['successful']}</span></p>
            <p>Failed: <span class="failed">{self.report_data['summary']['failed']}</span></p>
            <p>Total records: <strong>{self.report_data['summary']['total_records']}</strong></p>
            <p>Missing values: <strong>{self.report_data['summary']['missing_values']}</strong></p>
        </div>
        
        <h2>📋 Ticker Details</h2>
        <table>
            <tr>
                <th>Symbol</th>
                <th>Name</th>
                <th>Status</th>
                <th>Records</th>
                <th>Missing</th>
            </tr>
"""
        
        for symbol, data in self.report_data["tickers"].items():
            status = '<span class="success">✅ Success</span>' if data["success"] else '<span class="failed">❌ Error</span>'
            html += f"""
            <tr>
                <td>{symbol}</td>
                <td>{data['name']}</td>
                <td>{status}</td>
                <td>{data['records']}</td>
                <td>{data['missing_values']}</td>
            </tr>
"""
        
        html += """
        </table>
"""
        
        if self.report_data["errors"]:
            html += """
        <h2>⚠️ Errors</h2>
"""
            for error in self.report_data["errors"]:
                html += f'        <div class="error">{error}</div>\n'
        
        html += """
        <div class="footer">
            <p>Yahoo Finance Scraper v.1.5.0 | GNU GPL v3.0</p>
            <p>© 2025 Tomasz Lebioda</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def generate_text_report(self):
        text = f"""YAHOO FINANCE SCRAPER REPORT
{'=' * 50}
Execution time: {self.report_data['timestamp']}
Data range: {self.report_data['start_date']} - {self.report_data['date']}

SUMMARY
{'-' * 50}
Total tickers: {self.report_data['summary']['total_tickers']}
Successfully downloaded: {self.report_data['summary']['successful']}
Failed: {self.report_data['summary']['failed']}
Total records: {self.report_data['summary']['total_records']}
Missing values: {self.report_data['summary']['missing_values']}

TICKER DETAILS
{'-' * 50}
"""
        
        for symbol, data in self.report_data["tickers"].items():
            status = "SUCCESS" if data["success"] else "ERROR"
            text += f"{symbol:<12} {data['name']:<30} {status:<8} Records: {data['records']:<6} Missing: {data['missing_values']}\n"
        
        if self.report_data["errors"]:
            text += f"\nERRORS\n{'-' * 50}\n"
            for error in self.report_data["errors"]:
                text += f"- {error}\n"
        
        text += f"\n{'=' * 50}\nYahoo Finance Scraper v.1.5.0 | GNU GPL v3.0\n"
        return text
    
    def save_reports(self):
        # Create reports directory if it doesn't exist
        Path(REPORT_DIR).mkdir(exist_ok=True)
        
        date_str = self.report_data['date']
        
        # Save HTML report
        html_path = Path(REPORT_DIR) / f"report_{date_str}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_html_report())
        
        # Save text report
        text_path = Path(REPORT_DIR) / f"report_{date_str}.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_text_report())
        
        # Save JSON report
        json_path = Path(REPORT_DIR) / f"report_{date_str}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, ensure_ascii=False, indent=2)
        
        return html_path, text_path, json_path
    
    def send_email(self, text_report):
        """Tries to send email using mail command"""
        subject = f"Yahoo Finance Scraper Report - {self.report_data['date']}"
        
        try:
            # Check if mail command exists
            result = subprocess.run(['which', 'mail'], capture_output=True, text=True)
            if result.returncode != 0:
                print("Yahoo Finance Scraper: ⚠️ 'mail' command not available - report saved locally only")
                return False
            
            # Send email
            process = subprocess.Popen(
                ['mail', '-s', subject, EMAIL_TO],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(input=text_report)
            
            if process.returncode == 0:
                print(f"Yahoo Finance Scraper: ✉️ Report sent to {EMAIL_TO}")
                return True
            else:
                print("Yahoo Finance Scraper: ⚠️ Email sending error - report saved locally only")
                return False
                
        except Exception as e:
            print(f"Yahoo Finance Scraper: ⚠️ Email sending error: {e}")
            return False

# Initialize report generator
report = ReportGenerator()

# 1) Load existing data if file exists
if os.path.exists(OUTPUT_FILE):
    df_existing = pd.read_csv(OUTPUT_FILE, parse_dates=["date"], index_col="date")
else:
    df_existing = None

# 2) Prepare full date range from START_DATE to today
end_date = get_today_date()
all_dates = pd.date_range(start=START_DATE, end=end_date, freq='D', tz=None)
result_df = pd.DataFrame(index=all_dates)

print("Yahoo Finance Scraper: 🚀 Gathering data from Yahoo Finance...\n")

# 3) For each ticker download history and merge with existing data
for symbol, (col_name, decimals) in TICKER_CONFIG.items():
    print(f"Yahoo Finance Scraper: ⏳ Downloading {col_name} ({symbol})...", end=" ")
    
    try:
        # Download historical Close with backoff retry
        hist = fetch_with_backoff(symbol, START_DATE, end_date)
        
        if not hist.empty:
            print("✅")
            success = True
            error = None
        else:
            print("⚠️ (skipped/empty)")
            success = False
            error = "No data returned"
    except Exception as e:
        print("❌ (error)")
        success = False
        error = str(e)
        hist = pd.DataFrame()

    # Remove timezone if we have DatetimeIndex
    if isinstance(hist.index, pd.DatetimeIndex):
        hist.index = hist.index.tz_localize(None)

    # Prepare series with history
    if not hist.empty:
        series_new = hist["Close"].rename(col_name).round(decimals)
    else:
        series_new = pd.Series(name=col_name, dtype=float)

    # Reindex to full date range
    series_new = series_new.reindex(all_dates)

    # If there was previous data, merge: new overwrites, old preserved
    if df_existing is not None and col_name in df_existing.columns:
        series_existing = df_existing[col_name].reindex(all_dates)
        combined = series_new.combine_first(series_existing)
    else:
        combined = series_new

    # Add to result DF
    result_df[col_name] = combined
    
    # Collect statistics for report
    records_count = combined.notna().sum()
    missing_count = combined.isna().sum()
    report.add_ticker_result(symbol, col_name, success, records_count, missing_count, error)

# 4) Save result to CSV
result_df = result_df.reset_index().rename(columns={"index": "date"})
result_df["date"] = result_df["date"].dt.strftime("%Y-%m-%d")
result_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nYahoo Finance Scraper: 🎉 Done. Written to {OUTPUT_FILE} from {START_DATE} to {end_date} 📈")

# Generate and save reports
print("\nYahoo Finance Scraper: 📝 Generating reports...")
html_path, text_path, json_path = report.save_reports()
print(f"Yahoo Finance Scraper: 💾 Reports saved in '{REPORT_DIR}' directory")

# Try to send email
text_report = report.generate_text_report()
report.send_email(text_report)
