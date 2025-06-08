#!/bin/bash
cd /root/yahoo-scraper/
echo "[$(date)] Startuję skrypt pobierający dane z Yahoo! Finance" >> /var/log/crypto_scraper.log
/usr/bin/python3 yahoo-scraper.py >> /var/log/yahoo-scraper.log 2>&1
