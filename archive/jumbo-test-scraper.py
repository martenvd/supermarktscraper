import requests
from bs4 import BeautifulSoup
import json
import re
import mysql.connector as mariadb

# TODO: producten naar dedatabase schrijven

jumbo_url = "https://www.jumbo.com"
product_suffix = "/producten/?PageNumber="

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    #"X-Requested-With": "XMLHttpRequest"
}

all_products_reached = False
all_pages_reached = False
product_index = 0
page_index = 1

while not all_pages_reached:
    r = requests.get(jumbo_url + product_suffix + str(page_index), headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    if len(r.text) > 2200:
        while not all_products_reached:
            try:
                productnaam = soup.find_all("a", href=True)[product_index].text
                price_comp = soup.find_all("span", class_="jum-price-format jum-comparative-price")[product_index].text
                product_link = soup.find_all("a", href=True)[product_index]['href']
                price = soup.find_all("span", class_="jum-price-format")[product_index].text
                hoeveelheid = soup.find_all("span", class_="jum-pack-size")[product_index].text
                imagelink = re.findall("data-jum-hr-src=(.*?) ", str(soup.find_all("figure")[product_index]))[0].replace('"', '')
                #Probeer om de prijs naar euro's te berekenen. Soms is alleen de kilo/liter prijs gegeven. Dan lukt het niet.
                try:
                    price = int(price) / 100
                except:
                    pass
                print(productnaam, price, product_link, hoeveelheid, imagelink)
                product_index += 1
            except:
                all_products_reached = True
    else:
        all_pages_reached = True
    product_index = 0
    page_index += 1
    all_products_reached = False