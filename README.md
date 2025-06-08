# Yahoo Finance Scraper

![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)

## 📊 Project Description

Yahoo Finance Scraper is a tool for automatically downloading financial data from Yahoo Finance. The scraper collects currency rates, cryptocurrencies, stock indices, and stock prices of selected companies. Data is saved in CSV format and can be visualized using the included web dashboard.

## ✨ Features

- 🔄 Automatic data download from Yahoo Finance
- 💰 Currency rate support (USD/PLN, EUR/PLN, GBP/PLN)
- 🪙 Cryptocurrency tracking (Bitcoin, Ethereum, XRP, Solana, DOGE, USDT)
- 📈 Stock index monitoring (DAX, S&P 500, FTSE 100, Nikkei 225, WIG20, and others)
- 🏢 Stock price tracking (Tesla, Amazon)
- 📅 Automatic data updates from specified date
- 🛡️ Retry mechanism with exponential backoff for rate limiting handling
- 📊 Web dashboard with interactive charts
- 💾 Export data to CSV
- 🎨 Light/dark mode in dashboard
- 📧 Automatic execution reports (email/HTML/JSON)
- 📝 Detailed data download statistics

## 🚀 Installation

### Requirements

- Python 3.6+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yahoo-finance-scraper.git
cd yahoo-finance-scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 📋 Required Packages

- `yfinance` - main library for downloading data from Yahoo Finance
- `pandas` - data processing and analysis
- `pytz` - timezone support

## 🔧 Configuration

### Ticker Configuration

In the `scraper-yahoo-finance-all.py` file, you can customize the list of tracked financial instruments:

```python
TICKER_CONFIG = {
    "^GDAXI":   ("DAX", 2),                    # DAX Index
    "BTC-USD":  ("Bitcoin", 4),                # Bitcoin
    "PLN=X":    ("USD/PLN", 4),                # USD/PLN rate
    # Add your own tickers...
}
```

Format: `"TICKER": ("Name in CSV", decimal_places)`

### Date Configuration

The default start date is 2025-01-01. You can change it in the file:

```python
START_DATE = "2025-01-01"
```

### Report Configuration

Reports are generated automatically after each run:

```python
REPORT_DIR = "reports"                    # Reports directory
EMAIL_TO = "tomasz.lebioda@wyborcza.pl"  # Email address for reports
```

## 📖 Usage

### Manual Scraper Execution

```bash
python scraper-yahoo-finance-all.py
```

The script will download data from `START_DATE` to today and save it in the `scraped-data.csv` file.
Additionally, it will generate an execution report in HTML, TXT, and JSON formats in the `reports/` directory.
If the `mail` command is available on the server, the report will be sent via email.

### Automation with Cron

Add the following entries to crontab for automatic execution:

```bash
# Run scraper daily at 23:05
5 23 * * * /path/to/run_yahoo-finance-all.sh 2>&1 | while IFS= read -r line; do printf "%s %s\n" "$(date '+\%Y-%m-%d %H:%M:%S')" "$line"; done >> /var/log/scraper-yahoo-finance-all.log

# Copy CSV file to public location at 23:10
10 23 * * * cp /path/to/scraper-yahoo-finance-all/scraped-data.csv /where/file/should/be/scraped-data.csv
```

### Web Dashboard

1. Place `index.html` and `scraped-data.csv` (or `gw-scraped-data.csv`) files on a web server
2. Open `index.html` in a browser
3. The dashboard will automatically load and display the data

## 📊 Data Format

Data is saved in CSV format with the following structure:

```csv
date,DAX,China Shanghai SE Composite,the UK FTSE 100,...
2025-01-01,18000.50,3200.75,7500.25,...
2025-01-02,18050.75,3205.50,7510.50,...
```

## 🛡️ Error Handling

The scraper implements an advanced rate limiting handling mechanism:

- **Exponential backoff**: wait time doubles after each failed attempt
- **Jitter**: random delay ±20% prevents request synchronization
- **Throttling**: 1-5 second delay between tickers
- **Max retries**: maximum 5 attempts per ticker

## 🎨 Dashboard Features

- **Search**: filter data in the table
- **Sorting**: click column header to sort
- **Charts**: select indices to display on the chart
- **Export**: export filtered data to CSV
- **Chart export**: save chart as SVG
- **Date range**: set date range for export and charts
- **Dark/light mode**: toggle interface theme

## 📧 Reports

After each run, the scraper generates a detailed report containing:

- **Summary**: number of tickers, successes, errors
- **Statistics**: total number of records, missing values
- **Details for each ticker**: status, number of downloaded records
- **Error list**: if problems occurred

Reports are saved in three formats:
- `report_YYYY-MM-DD.html` - readable HTML report
- `report_YYYY-MM-DD.txt` - text report (sent via email)
- `report_YYYY-MM-DD.json` - data in JSON format

### Email Delivery

If the `mail` command is installed and configured on the VPS server, the report will be automatically sent to the email address specified in the configuration. Otherwise, reports will only be available locally in the `reports/` directory.

## 📁 Project Structure

```
scraper-yahoo-finance/
├── scraper-yahoo-finance-all.py    # Main scraper script
├── run_yahoo-finance-all.sh        # Helper script for running
├── index.html                      # Web dashboard
├── serve-csv.php                   # Optional PHP script for serving CSV
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── LICENSE                         # GNU GPL v3 license
├── scraped-data.csv               # Data file (generated)
└── reports/                        # Reports directory (generated)
    ├── report_YYYY-MM-DD.html     # HTML report
    ├── report_YYYY-MM-DD.txt      # Text report
    └── report_YYYY-MM-DD.json     # JSON report
```

## 🔒 Security

- The `serve-csv.php` script includes protection against "path traversal"
- Data is downloaded only from the official Yahoo Finance API
- No sensitive data is stored

## 🤝 Contributing

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is available under the GNU General Public License v3.0. See the `LICENSE` file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## 👤 Author

**Tomasz Lebioda**
- Email: tlebioda@gmail.com

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for the excellent Yahoo Finance API
- [Chart.js](https://www.chartjs.org/) for the charting library
- [Papa Parse](https://www.papaparse.com/) for CSV parsing in JavaScript

## ⚠️ Legal Notice

This project is intended for educational and non-commercial purposes only. Make sure to comply with Yahoo Finance's terms of use when using this tool.