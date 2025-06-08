#!/bin/bash
# Yahoo Finance Scraper - Run Script
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

cd /root/yahoo-scraper/
echo "[$(date)] Startuję skrypt pobierający dane z Yahoo! Finance" >> /var/log/crypto_scraper.log
/usr/bin/python3 yahoo-scraper.py >> /var/log/yahoo-scraper.log 2>&1
