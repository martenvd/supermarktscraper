import requests
from bs4 import BeautifulSoup
import json
import mysql.connector as mariadb
import time
import re


### MAIN CLASS ###

class Main_Scraper:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.headers = {}
        self.mariadb_connection = mariadb.connect(user="s4dpython", password="s4dpython", database="producten")
        self.cursor = self.mariadb_connection.cursor()

    def __repr__(self):
        return "Scraper class voor : " + self.name

    def soep(self, url, soepOfNiet):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        soup.encode('UTF-8')
        if soepOfNiet:
            return soup
        else:
            return r




### JUMBO ###

class Jumbo_Product_Scraper(Main_Scraper):
    def __init__(self, name, url):
        super().__init__(name, url)
        self.products = []
        self.product_suffix = "/producten/?PageNumber="
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}

    def get_jumbo_products(self):
        all_products_reached = False
        all_pages_reached = False
        product_index = 0
        page_index = 1

        while not all_pages_reached:
            # Delay om meer human te lijken.
            time.sleep(1)
            r = self.soep(self.url + self.product_suffix + str(page_index), False)
            soup = self.soep(self.url + self.product_suffix + str(page_index), True)
            #r = requests.get(self.url + self.product_suffix + str(page_index), headers=self.headers)
            #soup = BeautifulSoup(r.text, "lxml")
            if len(r.text) > 2200:
                while not all_products_reached:
                    try:
                        productnaam = soup.find_all("a", href=True)[product_index].text
                        product_url = soup.find_all("a", href=True)[product_index]['href']
                        prijs = soup.find_all("span", class_="jum-price-format")[product_index].text
                        hoeveelheid = soup.find_all("span", class_="jum-pack-size")[product_index].text
                        imagelink = re.findall("data-jum-hr-src=(.*?) ", str(soup.find_all("figure")[product_index]))[
                            0].replace('"', '')
                        try:
                            price = int(prijs) / 100
                        except:
                            pass
                        dict_string = {'productnaam': productnaam, 'prijs': prijs, 'product_url': product_url,
                                       'imagelink': imagelink, 'hoeveelheid': hoeveelheid}
                        self.products.append(dict_string)
                        print(self.products)
                        product_index += 1
                        self.cursor.execute(
                            "INSERT INTO jumbo (productnaam, prijs, product_url, hoeveelheid, imagelink) VALUES (%s, %s, %s, %s, %s)",
                            (productnaam, prijs, product_url, hoeveelheid, imagelink))
                        self.mariadb_connection.commit()
                    except:
                        all_products_reached = True
            else:
                all_pages_reached = True
            product_index = 0
            page_index += 1
            all_products_reached = False




### ALBERT HEIJN ###

class AH_Product_Scraper(Main_Scraper):
    def __init__(self, name, url):
        super().__init__(name, url)
        self.suffix = '/producten'
        self.categorie_url_list = []
        self.categorie_list = []
        self.producten_url_list = []

    def scraper(self):
        for a in self.soep(self.url + self.suffix, True).find_all('a', href=True):
            if "/producten/" in a['href'] and "/merk" not in a['href'] and "/eerder-gekocht" not in a['href']:
                self.categorie_url_list.append(self.url + a['href'])
                print(self.url + a['href'])

        self.categorie_url_list = list(set(self.categorie_url_list))


        for link in self.categorie_url_list:
            for a in self.soep(link + '?page=2000', True).find_all('a', href=True):
                if "/producten/product" in a['href']:
                    self.producten_url_list.append(self.url + a['href'])
                    print(self.url + a['href'])

        self.producten_url_list = list(set(self.producten_url_list))

        for link in self.producten_url_list:
            element = self.soep(link, True).find("script", type="application/ld+json").text
            element = json.loads(element)
            if 'offers' in element:
                productnaam = element['name']
                prijs = element['offers']['price']
                product_url = element['url']
                gewicht = element['weight']
                imagelink = element['image']
                self.cursor.execute(
                    "INSERT INTO albert_heijn (productnaam, prijs, product_url, hoeveelheid, imagelink) VALUES (%s, %s, %s, %s, %s)",
                    (productnaam, prijs, product_url, gewicht, imagelink))
                self.mariadb_connection.commit()
                print(element['name'], element['offers']['price'])




### ALDI ###

class Aldi_Product_Scraper(Main_Scraper):
    def __init__(self, name, url):
        super().__init__(name, url)
        self.categories = self.get_aldi_categories()
        self.products = []

    def get_aldi_categories(self):
        temp_list = []
        for a in self.soep(self.url, True).find_all('a', href=True):
            if "/onze-producten/" in a['href']:
                temp_list.append(self.url + a['href'])
        temp_list = list(set(temp_list))
        return temp_list

    def get_aldi_product(self):
        for categorie in self.categories:
            categorie_url = categorie
            #Delay om human te lijken.
            time.sleep(0.5)
            element = self.soep(categorie_url, True).find_all("script", type="application/ld+json")[-1].text
            element = json.loads(element)
            try:
                num_items = element['numberOfItems']
                #for i in range(0, num_items):
                for i in range(0, 1):
                    productnaam = element['itemListElement'][i]['name']
                    prijs = element['itemListElement'][i]['offers']['price']
                    product_url = element['itemListElement'][i]['url']
                    imagelink = element['itemListElement'][i]['image']
                    dict_string = {'productnaam': productnaam, 'prijs': prijs, 'product_url': product_url, 'imagelink': imagelink}
                    self.products.append(dict_string)
                    self.cursor.execute(
                        "INSERT INTO aldi (productnaam, prijs, product_url, imagelink) VALUES (%s, %s, %s, %s)",
                        (productnaam, prijs, product_url, imagelink))
                    self.mariadb_connection.commit()
                    #print(productnaam, prijs, product_url, imagelink)
            except:
                pass



#jumbo = Jumbo_Product_Scraper("Jumbo", "https://www.jumbo.com/")
#albert_heijn = AH_Product_Scraper("Albert Heijn", "https://www.ah.nl")
#aldi = Aldi_Product_Scraper("Aldi", "https://www.aldi.nl/")


#jumbo.get_jumbo_products()
#albert_heijn.scraper()
#aldi.get_aldi_product()

#ah_scraper.scraper()