import requests
from bs4 import BeautifulSoup
import json
import re
import mysql.connector as mariadb
import time

# TODO: producten naar database schrijven.

class jumbo_product_scraper:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.products = []
        self.product_suffix = "/producten/?PageNumber="
        self.headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" }

    def __repr__(self):
        return "Scraper class voor : " + self.name

    def get_jumbo_products(self):
        all_products_reached = False
        all_pages_reached = False
        product_index = 0
        page_index = 1

        while not all_pages_reached:
            #Delay om meer human te lijken.
            time.sleep(1)
            r = requests.get(self.url + self.product_suffix + str(page_index), headers=self.headers)
            soup = BeautifulSoup(r.text, "lxml")
            if len(r.text) > 2200:
                while not all_products_reached:
                    try:
                        productnaam = soup.find_all("a", href=True)[product_index].text
                        #price_comp = soup.find_all("span", class_="jum-price-format jum-comparative-price")[product_index].text
                        product_url = soup.find_all("a", href=True)[product_index]['href']
                        price = soup.find_all("span", class_="jum-price-format")[product_index].text
                        hoeveelheid = soup.find_all("span", class_="jum-pack-size")[product_index].text
                        imagelink = re.findall("data-jum-hr-src=(.*?) ", str(soup.find_all("figure")[product_index]))[0].replace('"', '')
                        try:
                            price = int(price) / 100
                        except:
                            pass
                        dict_string = {'productnaam': productnaam, 'prijs': price, 'product_url': product_url, 'imagelink': imagelink, 'hoeveelheid': hoeveelheid}
                        self.products.append(dict_string)
                        print(self.products)
                        product_index += 1
                    except:
                        all_products_reached = True
            else:
                all_pages_reached = True
            product_index = 0
            page_index += 1
            all_products_reached = False


jumbo = jumbo_product_scraper("Jumbo", "https://www.jumbo.com")
jumbo.get_jumbo_products()