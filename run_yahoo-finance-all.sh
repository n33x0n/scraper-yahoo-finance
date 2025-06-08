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

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create logs directory if it doesn't exist
mkdir -p logs

echo "[$(date)] Starting Yahoo! Finance data download script"
echo "[$(date)] Starting Yahoo! Finance data download script" >> logs/scraper-yahoo-finance-all.log

# Run the Python script and show output on screen AND in log file
python3 scraper-yahoo-finance-all.py 2>&1 | tee -a logs/scraper-yahoo-finance-all.log
