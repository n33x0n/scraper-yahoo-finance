W Crontabie muszą znaleźć się wpisy (codziennie o 21 odpalenie skryptu, codziennie o 21:30 kopiowanie pliku .csv z danymi do lokalizacji, z której jest wystawiany “na świat”):
0 21 * * * /root/indxscrp/run_scraper.sh >> /var/log/index_scraper.log 2>&1
30 21 * * * cp /root/indxscrp/index_data.csv /cytrus/index-scraper/index_data.csv