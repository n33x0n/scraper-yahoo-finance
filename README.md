# Yahoo Finance Scraper

![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)

## 📊 Opis projektu

Yahoo Finance Scraper to narzędzie do automatycznego pobierania danych finansowych z Yahoo Finance. Scraper zbiera kursy walut, kryptowalut, indeksów giełdowych oraz cen akcji wybranych spółek. Dane są zapisywane w formacie CSV i mogą być wizualizowane za pomocą dołączonego dashboardu webowego.

## ✨ Funkcjonalności

- 🔄 Automatyczne pobieranie danych z Yahoo Finance
- 💰 Obsługa kursów walut (USD/PLN, EUR/PLN, GBP/PLN)
- 🪙 Śledzenie kryptowalut (Bitcoin, Ethereum, XRP, Solana, DOGE, USDT)
- 📈 Monitorowanie indeksów giełdowych (DAX, S&P 500, FTSE 100, Nikkei 225, WIG20 i inne)
- 🏢 Śledzenie cen akcji (Tesla, Amazon)
- 📅 Automatyczna aktualizacja danych od określonej daty
- 🛡️ Mechanizm retry z exponential backoff dla obsługi rate limiting
- 📊 Dashboard webowy z interaktywnymi wykresami
- 💾 Eksport danych do CSV
- 🎨 Tryb jasny/ciemny w dashboardzie
- 📧 Automatyczne raporty z wykonania (email/HTML/JSON)
- 📝 Szczegółowe statystyki pobierania danych

## 🚀 Instalacja

### Wymagania

- Python 3.6+
- pip (menedżer pakietów Python)

### Kroki instalacji

1. Sklonuj repozytorium:
```bash
git clone https://github.com/yourusername/yahoo-finance-scraper.git
cd yahoo-finance-scraper
```

2. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

## 📋 Wymagane pakiety

- `yfinance` - główna biblioteka do pobierania danych z Yahoo Finance
- `pandas` - przetwarzanie i analiza danych
- `pytz` - obsługa stref czasowych

## 🔧 Konfiguracja

### Konfiguracja tickerów

W pliku `scraper-yahoo-finance-all.py` możesz dostosować listę śledzonych instrumentów finansowych:

```python
TICKER_CONFIG = {
    "^GDAXI":   ("DAX", 2),                    # Indeks DAX
    "BTC-USD":  ("Bitcoin", 4),                # Bitcoin
    "PLN=X":    ("USD/PLN", 4),                # Kurs USD/PLN
    # Dodaj własne tickery...
}
```

Format: `"TICKER": ("Nazwa w CSV", liczba_miejsc_po_przecinku)`

### Konfiguracja dat

Domyślna data początkowa to 2025-01-01. Możesz ją zmienić w pliku:

```python
START_DATE = "2025-01-01"
```

### Konfiguracja raportów

Raporty są generowane automatycznie po każdym uruchomieniu:

```python
REPORT_DIR = "reports"                    # Katalog z raportami
EMAIL_TO = "tomasz.lebioda@wyborcza.pl"  # Adres email dla raportów
```

## 📖 Użycie

### Ręczne uruchomienie scrapera

```bash
python scraper-yahoo-finance-all.py
```

Skrypt pobierze dane od `START_DATE` do dnia dzisiejszego i zapisze je w pliku `scraped-data.csv`. 
Dodatkowo wygeneruje raport z wykonania w formacie HTML, TXT i JSON w katalogu `reports/`.
Jeśli na serwerze jest dostępna komenda `mail`, raport zostanie wysłany mailem.

### Automatyzacja z wykorzystaniem Cron

Dodaj następujące wpisy do crontab dla automatycznego uruchamiania:

```bash
# Uruchomienie scrapera codziennie o 23:05
5 23 * * * /sciezka/do/run_yahoo-finance-all.sh 2>&1 | while IFS= read -r line; do printf "%s %s\n" "$(date '+\%Y-%m-%d %H:%M:%S')" "$line"; done >> /var/log/scraper-yahoo-finance-all.log

# Kopiowanie pliku CSV do lokalizacji publicznej o 23:10
10 23 * * * cp /sciezka/do/scraper-yahoo-finance-all/scraped-data.csv /gdzie/ma/lezec/plik/scraped-data.csv
```

### Dashboard webowy

1. Umieść pliki `index.html` i `scraped-data.csv` (lub `gw-scraped-data.csv`) na serwerze webowym
2. Otwórz `index.html` w przeglądarce
3. Dashboard automatycznie załaduje i wyświetli dane

## 📊 Format danych

Dane są zapisywane w formacie CSV z następującą strukturą:

```csv
date,DAX,China Shanghai SE Composite,the UK FTSE 100,...
2025-01-01,18000.50,3200.75,7500.25,...
2025-01-02,18050.75,3205.50,7510.50,...
```

## 🛡️ Obsługa błędów

Scraper implementuje zaawansowany mechanizm obsługi rate limiting:

- **Exponential backoff**: czas oczekiwania podwaja się po każdej nieudanej próbie
- **Jitter**: losowe opóźnienie ±20% zapobiega synchronizacji requestów
- **Throttling**: opóźnienie 1-5 sekund między tickerami
- **Max retries**: maksymalnie 5 prób na ticker

## 🎨 Dashboard - funkcjonalności

- **Wyszukiwanie**: filtrowanie danych w tabeli
- **Sortowanie**: kliknij nagłówek kolumny aby posortować
- **Wykresy**: wybierz indeksy do wyświetlenia na wykresie
- **Eksport**: eksportuj przefiltrowane dane do CSV
- **Eksport wykresu**: zapisz wykres jako SVG
- **Zakres dat**: ustaw zakres dat dla eksportu i wykresów
- **Tryb ciemny/jasny**: przełączanie motywu interfejsu

## 📧 Raporty

Po każdym uruchomieniu scraper generuje szczegółowy raport zawierający:

- **Podsumowanie**: liczba tickerów, sukcesy, błędy
- **Statystyki**: łączna liczba rekordów, brakujące wartości
- **Szczegóły każdego tickera**: status, liczba pobranych rekordów
- **Lista błędów**: jeśli wystąpiły problemy

Raporty są zapisywane w trzech formatach:
- `report_YYYY-MM-DD.html` - czytelny raport HTML
- `report_YYYY-MM-DD.txt` - raport tekstowy (wysyłany mailem)
- `report_YYYY-MM-DD.json` - dane w formacie JSON

### Wysyłka emailem

Jeśli na serwerze VPS jest zainstalowana i skonfigurowana komenda `mail`, raport zostanie automatycznie wysłany na adres email podany w konfiguracji. W przeciwnym razie raporty będą dostępne tylko lokalnie w katalogu `reports/`.

## 📁 Struktura projektu

```
scraper-yahoo-finance/
├── scraper-yahoo-finance-all.py    # Główny skrypt scrapera
├── run_yahoo-finance-all.sh        # Skrypt pomocniczy do uruchamiania
├── index.html                      # Dashboard webowy
├── serve-csv.php                   # Opcjonalny skrypt PHP do serwowania CSV
├── requirements.txt                # Zależności Python
├── README.md                       # Dokumentacja
├── LICENSE                         # Licencja GNU GPL v3
├── scraped-data.csv               # Plik z danymi (generowany)
└── reports/                        # Katalog z raportami (generowany)
    ├── report_YYYY-MM-DD.html     # Raport HTML
    ├── report_YYYY-MM-DD.txt      # Raport tekstowy
    └── report_YYYY-MM-DD.json     # Raport JSON
```

## 🔒 Bezpieczeństwo

- Skrypt `serve-csv.php` zawiera zabezpieczenie przed "path traversal"
- Dane są pobierane tylko z oficjalnego API Yahoo Finance
- Brak przechowywania danych wrażliwych

## 🤝 Wkład w projekt

1. Fork repozytorium
2. Stwórz branch dla swojej funkcjonalności (`git checkout -b feature/AmazingFeature`)
3. Commit zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Push do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📝 Licencja

Projekt jest dostępny na licencji GNU General Public License v3.0. Zobacz plik `LICENSE` dla szczegółów.

Ten program jest wolnym oprogramowaniem: możesz go rozpowszechniać i/lub modyfikować zgodnie z warunkami Powszechnej Licencji Publicznej GNU opublikowanej przez Free Software Foundation, w wersji 3 tej Licencji lub (według twojego wyboru) dowolnej późniejszej wersji.

## 👤 Autor

**Tomasz Lebioda**
- Email: tlebioda@gmail.com

## 🙏 Podziękowania

- [yfinance](https://github.com/ranaroussi/yfinance) za świetne API do Yahoo Finance
- [Chart.js](https://www.chartjs.org/) za bibliotekę wykresów
- [Papa Parse](https://www.papaparse.com/) za parsowanie CSV w JavaScript

## ⚠️ Uwagi prawne

Ten projekt jest przeznaczony wyłącznie do celów edukacyjnych i niekomercyjnych. Upewnij się, że przestrzegasz warunków użytkowania Yahoo Finance przy korzystaniu z tego narzędzia.