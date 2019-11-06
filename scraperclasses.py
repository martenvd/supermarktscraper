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

    def soup(self, url, soupOrNot):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        soup.encode('UTF-8')
        if soupOrNot:
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
            r = self.soup(self.url + self.product_suffix + str(page_index), False)
            soup = self.soup(self.url + self.product_suffix + str(page_index), True)
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
        for a in self.soup(self.url + self.suffix, True).find_all('a', href=True):
            if "/producten/" in a['href'] and "/merk" not in a['href'] and "/eerder-gekocht" not in a['href']:
                self.categorie_url_list.append(self.url + a['href'])
                print(self.url + a['href'])

        self.categorie_url_list = list(set(self.categorie_url_list))

        for link in self.categorie_url_list:
            for a in self.soup(link + '?page=2000', True).find_all('a', href=True):
                if "/producten/product" in a['href']:
                    self.producten_url_list.append(self.url + a['href'])
                    print(self.url + a['href'])

        self.producten_url_list = list(set(self.producten_url_list))

        try:
            for link in self.producten_url_list:
                element = self.soup(link, True).find("script", type="application/ld+json").text
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
        except:
            pass



### ALDI ###

class Aldi_Product_Scraper(Main_Scraper):
    def __init__(self, name, url):
        super().__init__(name, url)
        self.categories = self.get_aldi_categories()
        self.products = []

    def get_aldi_categories(self):
        temp_list = []
        for a in self.soup(self.url, True).find_all('a', href=True):
            if "/onze-producten/" in a['href']:
                temp_list.append(self.url + a['href'])
        temp_list = list(set(temp_list))
        return temp_list

    def get_aldi_product(self):
        for categorie in self.categories:
            categorie_url = categorie
            #Delay om human te lijken.
            time.sleep(0.5)
            element = self.soup(categorie_url, True).find_all("script", type="application/ld+json")[-1].text
            element = json.loads(element)
            try:
                num_items = element['numberOfItems']
                for i in range(0, num_items):
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


### COOP CLASS ####

class Coop_Product_Scraper(Main_Scraper):
    products = []

    def __init__(self, name, url):
        super().__init__(name, url)
        self.suffix = '/boodschappen/'
        self.fetch_all()

    #def parse_page(self, url):
        #page = requests.get(url)
        #soup = BeautifulSoup(page.text, 'html.parser')
        #soup.encode('UTF-8')
        #return soup

    def fetch_categories(self):
        categories = []
        for link in self.soup(self.url + self.suffix, True).find_all('a', href=True):
            if '/boodschappen/' in link['href']:
                categories.append(link['href'])
        categories = list(set(categories))
        return categories


    def fetch_products(self, category_url):
        page = self.soup(category_url + "?PageSize=99999", True)  # haal pagina met producten in categorie op
        for article in page.find_all('article'):  # loop over alle producten heen
            try:
                img = article.find('img')['data-srcset'].split()[0]  # afbeelding van product
                data = json.loads(article['data-product'])  # {"id":"3509","price":"1.69","list":"product-category","variant":"1 stuk(s)"}
                name = article.find('h2')['title']  # naam van product
                product_url = article.find('a')['href']
                hoeveelheid = data['variant']
                prijs = float(data['price'])
                product = {
                    'id': data['id'], # heeft ah dit ook?
                    'naam': name,
                    'prijs': float(data['price']),
                    'product_url': product_url,
                    'hoeveelheid': data['variant'],
                    'image_url': img
                }
                self.products.append(product)
                try:
                    self.cursor.execute(
                        "INSERT INTO coop (productnaam, prijs, product_url, hoeveelheid, imagelink) VALUES (%s, %s, %s, %s, %s)",
                        (name, prijs, product_url, hoeveelheid, img))
                    self.mariadb_connection.commit()
                except mariadb.Error as err:
                    print(err)
            except:
                pass


    def fetch_all(self):
        categories = self.fetch_categories() # haal cat pagina op en parse alle categorieen
        for cat in categories:
            self.fetch_products(cat) # haal alle producten van cateegorieen op



#jumbo = Jumbo_Product_Scraper("Jumbo", "https://www.jumbo.com/")
#albert_heijn = AH_Product_Scraper("Albert Heijn", "https://www.ah.nl")
#aldi = Aldi_Product_Scraper("Aldi", "https://www.aldi.nl/")
#coop = Coop_Product_Scraper("COOP", "https://www.coop.nl")

#jumbo.get_jumbo_products()
#albert_heijn.scraper()
#aldi.get_aldi_product()
#print(coop.products)