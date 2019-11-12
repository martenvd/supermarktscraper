import requests
from bs4 import BeautifulSoup
import json
import mysql.connector as mariadb
import time
import re

# TODO: alles hieronder
# De Coop Scraper werkt niet naar behoren.
# Naamgeving Albert_Heijn categorielijsten aanpassen naar de standaard.
# Testen na de aanpassingen.

### Static Settings Class ###
class Settings:
    database_user = "s4dpython"
    database_password = "s4dpython"
    database_db = "producten"
    database_port = 3307
    database_host = "213.190.22.172"

### Product Class ###
class Product:
    def __init__(self, supermarket, name, price, quantity, url, image):
        self.supermarket = supermarket
        self.name = name
        self.price = price
        self.quantity = quantity
        self.url = url
        self.image = image

    def __repr__(self):
        return "Product Class for: {} from supermarket: {}.".format(self.name, self.supermarket)

### Static Database Class ###
class Database:
    def __init__(self, supermarket):
        self.supermarket = supermarket
        self.mariadb_connection = mariadb.connect(user=Settings.database_user, password=Settings.database_password,
                                                  database=Settings.database_db, host=Settings.database_host,
                                                  port=Settings.database_port)
        self.cursor = self.mariadb_connection.cursor()

    def __repr__(self):
        return "Database Class for: {}".format(self.supermarket)

    # TODO: advies vragen over de product.supermarket vs self.supermarket.
    #  Welke optie is beter? laten afhangen van het product of van de Class instance?
    def write_product(self, product):
        try:
            self.cursor.execute("INSERT INTO {} (productnaam, prijs, product_url, hoeveelheid, imagelink) "
                                "VALUES (%s, %s, %s, %s, %s)".format(product.supermarket),
                                (product.name, product.price, product.url, product.quantity, product.image))
            self.mariadb_connection.commit()
        except mariadb.Error as error:
            print(error)


### PARENT SCRAPER CLASS ###
class Scraper:
    def __init__(self, name, url, url_suffix, headers):
        self.name = name
        self.url = url
        self.url_suffix = url_suffix
        self.headers = headers
        self.table_name = self.name.lower()
        self.database = Database(self.table_name)
        self.products = []
        self.categories_url = []

    def __repr__(self):
        return "Scraper Class for: {}".format(self.name)

    def soup(self, url):
        response = self.response(url)
        soup = BeautifulSoup(response.text, 'lxml')
        soup.encode('UTF-8')
        return soup

    def response(self, url):
        return requests.get(url, headers=self.headers)


### JUMBO ###
class Jumbo_scraper(Scraper):
    def __init__(self):
        super().__init__(name="Jumbo", url="https://www.jumbo.com", url_suffix="/producten/?PageNumber=",
                         headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"})

    def fetch_all_products(self):
        all_products_reached = False
        all_pages_reached = False
        product_index = 0
        page_index = 1

        while not all_pages_reached:
            # Delay om meer human te lijken.
            print("[*] Jumbo / Scraping page {}/2105".format(page_index))
            time.sleep(1)
            response = self.response(self.url + self.url_suffix + str(page_index))
            soup = self.soup(self.url + self.url_suffix + str(page_index))
            if len(response.text) > 2200:
                while not all_products_reached:
                    try:
                        productnaam = soup.find_all("a", href=True)[product_index].text
                        product_url = soup.find_all("a", href=True)[product_index]['href']
                        prijs = soup.find_all("span", class_="jum-price-format")[product_index].text
                        hoeveelheid = soup.find_all("span", class_="jum-pack-size")[product_index].text
                        imagelink = re.findall("data-jum-hr-src=(.*?) ",
                                               str(soup.find_all("figure")[product_index]))[0].replace('"', '')

                        # TODO: wanneer de prijs per kilo/liter is iets verzinnen om te converten.
                        try:
                            prijs = int(prijs) / 100
                        except:
                            pass

                        product = Product(self.table_name, productnaam, prijs, hoeveelheid, product_url, imagelink)
                        self.products.append(product)
                        self.database.write_product(product)

                        product_index += 1
                    except:
                        all_products_reached = True
            else:
                all_pages_reached = True
                print("[*] Jumbo / Scraping stopped after {} pages".format(page_index))
            product_index = 0
            page_index += 1
            all_products_reached = False

### ALBERT HEIJN ###
class AH_scraper(Scraper):
    def __init__(self):
        super().__init__(name="Albert_Heijn", url="https://www.ah.nl", url_suffix="/producten",
                         headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"})
        self.categorie_url_list = []
        self.categorie_list = []
        self.producten_url_list = []

    def fetch_all_products(self):
        print("[*] AH / Indexing all categories")
        for a in self.soup(self.url + self.url_suffix).find_all('a', href=True):
            if "/producten/" in a['href'] and "/merk" not in a['href'] and "/eerder-gekocht" not in a['href']:
                self.categorie_url_list.append(self.url + a['href'])
        self.categorie_url_list = list(set(self.categorie_url_list))

        print("[*] AH / Indexing all product urls")
        for link in self.categorie_url_list:
            for a in self.soup(link + '?page=2000').find_all('a', href=True):
                if "/producten/product" in a['href']:
                    self.producten_url_list.append(self.url + a['href'])
        self.producten_url_list = list(set(self.producten_url_list))
        print("[*] AH / Number of products found: {}".format(len(self.producten_url_list)))

        try:
            print("[*] AH / Fetching all product information")
            for link in self.producten_url_list:
                time.sleep(0.2)
                print("[*] AH / Fetching {}".format(link))
                try:
                    element = self.soup(link).find("script", type="application/ld+json").text
                    element = json.loads(element)
                    if 'offers' in element:
                        productnaam = element['name']
                        prijs = element['offers']['price']
                        product_url = element['url']
                        hoeveelheid = element['weight']
                        imagelink = element['image']

                        product = Product(self.table_name, productnaam, prijs, hoeveelheid, product_url, imagelink)
                        self.products.append(product)
                        self.database.write_product(product)
                    else:
                        print("[-] AH / No Offer in element")
                except:
                    print("[-] AH / Product {} Failed".format(link))
        except:
            print("[*] AH / Stopped fetching all product information")
            pass

### ALDI ###
class Aldi_scraper(Scraper):
    def __init__(self):
        super().__init__(name="Aldi", url="https://www.aldi.nl", url_suffix=None,
                         headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"})
        self.fetch_all_categories()

    def fetch_all_categories(self):
        for a in self.soup(self.url).find_all('a', href=True):
            if "/onze-producten/" in a['href']:
                # Delay om human te lijken.
                time.sleep(0.1)
                self.categories_url.append(self.url + a['href'])
        self.categories_url = list(set(self.categories_url))

    def fetch_all_products(self):
        for link in self.categories_url:
            # Delay om human te lijken.
            time.sleep(5)
            print("[*] Aldi / Scraping categorie {}".format(link))
            element = self.soup(link).find_all("script", type="application/ld+json")[-1].text
            element = json.loads(element)
            try:
                num_items = element['numberOfItems']
                for i in range(0, num_items):
                    productnaam = element['itemListElement'][i]['name']
                    prijs = element['itemListElement'][i]['offers']['price']
                    product_url = element['itemListElement'][i]['url']
                    imagelink = element['itemListElement'][i]['image']

                    # TODO: hoeveelheid ophalen bij Aldi, is voor nu NULL.
                    # TODO: wanneer de prijs per kilo/liter is iets verzinnen om te converten.
                    product = Product(self.table_name, productnaam, prijs, "NULL", product_url, imagelink)
                    self.products.append(product)
                    self.database.write_product(product)
            except:
                pass


### COOP CLASS ####
class Coop_scraper(Scraper):
    def __init__(self):
        super().__init__(name="Coop", url="https://www.coop.nl", url_suffix="/boodschappen/",
                         headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"})
        self.fetch_all_categories()

    def fetch_all_categories(self):
        for link in self.soup(self.url + self.url_suffix).find_all('a', href=True):
            if "/boodschappen/" in link['href']:
                self.categories_url.append(link['href'])
        self.categories_url = list(set(self.categories_url))

    def fetch_all_products(self):
        for link in self.categories_url:
            # Delay om human te lijken.
            time.sleep(0.2)
            print("[*] Coop / Scraping categorie {}".format(link))
            page = self.soup(link + "?PageSize=99999")
            for article in page.find_all('article'):
                try:
                    img = article.find('img')['data-srcset'].split()[0]
                    data = json.loads(article['data-product'])
                    name = article.find('h2')['title']
                    product_url = article.find('a')['href']
                    hoeveelheid = data['variant']
                    prijs = float(data['price'])

                    product = Product(self.table_name, name, prijs, hoeveelheid, product_url, img)
                    self.products.append(product)
                    self.database.write_product(product)
                except:
                    pass