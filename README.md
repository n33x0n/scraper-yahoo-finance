W Crontabie muszą znaleźć się wpisy (codziennie o 23:05 odpalenie skryptu, codziennie o 23:10 kopiowanie pliku .csv z danymi do lokalizacji, z której jest wystawiany “na świat”):
5 23 * * * /sciezka/do/run_yahoo-finance-all.sh 2>&1 | while IFS= read -r line; do printf "%s %s\n" "$(date '+\%Y-%m-%d %H:%M:%S')" "$line"; done >> /var/log/scraper-yahoo-finance-all.log
10 23 * * * cp /sciezka/do/scraper-yahoo-finance-all/scraped-data.csv /gdzie/ma/lezec/plik/scraped-data.csv
