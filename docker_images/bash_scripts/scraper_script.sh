#!/bin/bash

# Clean log file
echo "" > /root/scraper_log.txt
echo "" > /root/validation/validate_log.txt

# Clean the Developement database
mysql -u s4dpython --password="s4dpython" -h 127.0.0.1 -P 3307 < /root/recreate_mysql.sql && echo "[**********] Dev DB (port 3307) cleaned - `date`[**********]" >> /root/scraper_log.txt

# Fill the Development database with products
echo "[**********] Starting scraperscript - `date` [**********]" >> /root/scraper_log.txt && python3 /home/s4d_python/main.py 2>&1 >> /root/scraper_log.txt

# Validate the scraped products before pushing to production
/root/validation/validate_database.sh
