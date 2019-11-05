import requests
from bs4 import BeautifulSoup
import json
import mysql.connector as mariadb


class AH_scraper:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.mariadb_connection = mariadb.connect(user="s4dpython", password="s4dpython", database="producten")
        self.cursor = self.mariadb_connection.cursor()
        self.categorie_url_list = []
        self.categorie_list = []
        self.producten_url_list = []

    def __repr__(self):
        return "Scraper class voor : " + self.name

    def soep(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        soup.encode('UTF-8')
        return soup

    def scraper(self):
        for a in self.soep(self.url).find_all('a', href=True):
            if "/producten/" in a['href'] and "/merk" not in a['href'] and "/eerder-gekocht" not in a['href']:
                self.categorie_url_list.append(self.url + a['href'])

        self.categorie_url_list = list(set(self.categorie_url_list))

        for link in self.categorie_url_list:
            for a in self.soep(link + '?page=2000').find_all('a', href=True):
                if "/producten/product" in a['href']:
                    self.producten_url_list.append(self.url + a['href'])

        self.producten_url_list = list(set(self.producten_url_list))

        for link in self.producten_url_list:
            element = self.soep(link).find("script", type="application/ld+json").text
            element = json.loads(element)
            if 'offers' in element:
                productnaam = element['name']
                prijs = element['offers']['price']
                product_url = element['url']
                gewicht = element['weight']
                imagelink = element['image']
                self.cursor.execute(
                    "INSERT INTO albert_heijn (productnaam, prijs, product_url, gewicht, imagelink) VALUES (%s, %s, %s, %s, %s)",
                    (productnaam, prijs, product_url, gewicht, imagelink))
                self.mariadb_connection.commit()
                print(element['name'], element['offers']['price'])


ah_scraper = AH_scraper("Albert Heijn", "https://www.ah.nl/producten")

ah_scraper.scraper()
