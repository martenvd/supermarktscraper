#!/bin/bash

echo "" > /root/validation/validate_log.txt
echo "[*****] Starting to validate the scraped products - `date` [*****]" >> /root/validation/validate_log.txt

aldi_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from aldi" | grep "[0-9]\{1,\}"`
jumbo_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from jumbo" | grep "[0-9]\{1,\}"`
ah_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from albert_heijn" | grep "[0-9]\{1,\}"`
coop_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from coop" | grep "[0-9]\{1,\}"`

aldi_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from aldi" | grep "[0-9]\{1,\}"`
jumbo_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from jumbo" | grep "[0-9]\{1,\}"`
ah_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from albert_heijn" | grep "[0-9]\{1,\}"`
coop_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from coop" | grep "[0-9]\{1,\}"`

echo "[*] Aldi_Dev: $aldi_count_dev 	|	 Aldi_Prod: $aldi_count_prod" >> /root/validation/validate_log.txt
echo "[*] Jumbo_Dev: $jumbo_count_dev 	|	 Jumbo_Prod: $jumbo_count_prod" >> /root/validation/validate_log.txt
echo "[*] AH_Dev: $ah_count_dev 	|	 AH_Prod: $ah_count_prod" >> /root/validation/validate_log.txt
echo "[*] Coop_Dev: $coop_count_dev 	|	 Coop_Prod: $coop_count_prod" >> /root/validation/validate_log.txt

marge=10
aldi_marge=$(($aldi_count_prod / $marge))
jumbo_marge=$(($jumbo_count_prod / $marge))
ah_marge=$(($ah_count_prod / $marge))
coop_marge=$(($coop_count_prod / $marge))

if [[ $(($aldi_count_prod - $aldi_marge)) -gt $aldi_count_dev ]]
then
	echo "[-] Scraping Aldi Failed!" >> /root/validation/validate_log.txt
	echo "[*] Restarting Aldi scraper in 15 minutes" >> /root/validation/validate_log.txt
	echo "[*] Aldi scraping failed, restarting the scrape in 15 minutes" >> /root/scraper_log.txt
	sleep 15m && echo "[+] Starting Aldi scrape - `date`" >> /root/scraper_log.txt && mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "DELETE FROM aldi" && python3 /home/s4d_python/main.py aldi 2>&1 >> /root/scraper_log.txt &
else
	echo "[+] Scraping Aldi Succeeded!" >> /root/validation/validate_log.txt
	echo "[*] Starting to migrate the Aldi-Data from Dev to Prod" >> /root/validation/validate_log.txt
	mysqldump -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 producten aldi > /root/validation/db_dumps/aldi_dev_dump.sql
	echo "[+] Dev data dumped!" >> /root/validation/validate_log.txt
	mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten < /root/validation/db_dumps/aldi_dev_dump.sql
	echo "[+] Aldi data migrated to Prod!" >> /root/validation/validate_log.txt
fi

if [[ $(($jumbo_count_prod - $jumbo_marge)) -gt $jumbo_count_dev ]]
then
        echo "[-] Scraping Jumbo Failed!" >> /root/validation/validate_log.txt
        echo "[*] Restarting Jumbo scraper in 15 minutes" >> /root/validation/validate_log.txt
        echo "[*] Jumbo scraping failed, restarting the scrape in 15 minutes" >> /root/scraper_log.txt
        sleep 15m && echo "[+] Starting Jumbo scrape - `date`" >> /root/scraper_log.txt && mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "DELETE FROM jumbo" && python3 /home/s4d_python/main.py jumbo 2>&1 >> /root/scraper_log.txt &
else
        echo "[+] Scraping Jumbo Succeeded!" >> /root/validation/validate_log.txt
        echo "[*] Starting to migrate the Jumbo-Data from Dev to Prod" >> /root/validation/validate_log.txt
	mysqldump -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 producten jumbo > /root/validation/db_dumps/jumbo_dev_dump.sql
	echo "[+] Dev data dumped!" >> /root/validation/validate_log.txt
        mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten < /root/validation/db_dumps/jumbo_dev_dump.sql
        echo "[+] Jumbo data migrated to Prod!" >> /root/validation/validate_log.txt
fi

if [[ $(($ah_count_prod - $ah_marge)) -gt $ah_count_dev ]]
then
        echo "[-] Scraping AH Failed!" >> /root/validation/validate_log.txt
        echo "[*] Restarting AH scraper in 15 minutes" >> /root/validation/validate_log.txt
        echo "[*] AH scraping failed, restarting the scrape in 15 minutes" >> /root/scraper_log.txt
        sleep 15m && echo "[+] Starting AH scrape - `date`" >> /root/scraper_log.txt && mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "DELETE FROM albert_heijn" && python3 /home/s4d_python/main.py albert_heijn 2>&1 >> /root/scraper_log.txt &
else
        echo "[+] Scraping AH Succeeded!" >> /root/validation/validate_log.txt
        echo "[*] Starting to migrate the AH_Data from Dev to Prod" >> /root/validation/validate_log.txt
	mysqldump -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 producten albert_heijn > /root/validation/db_dumps/ah_dev_dump.sql
	echo "[+] Dev data dumped!" >> /root/validation/validate_log.txt
        mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten < /root/validation/db_dumps/ah_dev_dump.sql
        echo "[+] AH data migrated to Prod!" >> /root/validation/validate_log.txt
fi

if [[ $(($coop_count_prod - $coop_marge)) -gt $coop_count_dev ]]
then
        echo "[-] Scraping Coop Failed!" >> /root/validation/validate_log.txt
        echo "[*] Restarting Coop scraper in 15 minutes" >> /root/validation/validate_log.txt
        echo "[*] Coop scraping failed, restarting the scrape in 15 minutes" >> /root/scraper_log.txt
        sleep 15m && echo "[+] Starting Coop scrape - `date`" >> /root/scraper_log.txt && mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "DELETE FROM coop" && python3 /home/s4d_python/main.py coop 2>&1 >> /root/scraper_log.txt &
else
        echo "[+] Scraping Coop Succeeded!" >> /root/validation/validate_log.txt
        echo "[*] Starting to migrate the Coop_Data from Dev to Prod" >> /root/validation/validate_log.txt
	mysqldump -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 producten coop > /root/validation/db_dumps/coop_dev_dump.sql
	echo "[+] Dev data dumped!" >> /root/validation/validate_log.txt
        mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten < /root/validation/db_dumps/coop_dev_dump.sql
        echo "[+] Coop data migrated to Prod!" >> /root/validation/validate_log.txt
fi

aldi_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from aldi" | grep "[0-9]\{1,\}"`
jumbo_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from jumbo" | grep "[0-9]\{1,\}"`
ah_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from albert_heijn" | grep "[0-9]\{1,\}"`
coop_count_dev=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3307 -D producten -e "SELECT count(*) from coop" | grep "[0-9]\{1,\}"`

aldi_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from aldi" | grep "[0-9]\{1,\}"`
jumbo_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from jumbo" | grep "[0-9]\{1,\}"`
ah_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from albert_heijn" | grep "[0-9]\{1,\}"`
coop_count_prod=`mysql -u s4dpython -ps4dpython -h 127.0.0.1 -P 3306 -D producten -e "SELECT count(*) from coop" | grep "[0-9]\{1,\}"`

echo "[*****] Database Stats after Validation & Migration [*****]" >> /root/validation/validate_log.txt

echo "[*] Aldi_Dev: $aldi_count_dev 	|	 Aldi_Prod: $aldi_count_prod" >> /root/validation/validate_log.txt
echo "[*] Jumbo_Dev: $jumbo_count_dev 	|	 Jumbo_Prod: $jumbo_count_prod" >> /root/validation/validate_log.txt
echo "[*] AH_Dev: $ah_count_dev 	|	 AH_Prod: $ah_count_prod" >> /root/validation/validate_log.txt
echo "[*] Coop_Dev: $coop_count_dev 	|	 Coop_Prod: $coop_count_prod" >> /root/validation/validate_log.txt

echo "[+] Database Validation and Migration Finished - `date`" >> /root/validation/validate_log.txt