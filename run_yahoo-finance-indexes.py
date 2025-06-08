#!/bin/bash

cd /yahoo-finance-indexes/ # ← zmień na właściwą ścieżkę
#source venv/bin/activate  # ← jeśli masz virtualenv, inaczej pomiń tę linię
/usr/bin/python3 scraper.py
