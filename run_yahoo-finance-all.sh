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
echo "[$(date)] Starting Yahoo! Finance data download script" >> /var/log/scraper-yahoo-finance-all.log
/usr/bin/python3 scraper-yahoo-finance-all.py >> /var/log/scraper-yahoo-finance-all.log 2>&1
