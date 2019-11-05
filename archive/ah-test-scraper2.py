import requests
from bs4 import BeautifulSoup
import json
import mysql.connector as mariadb


# mariadb_connection = mariadb.connect(user="s4dpython", password="s4dpython", database="producten")
ah_url = "https://www.ah.nl/producten/product"
# cursor = mariadb_connection.cursor()


class Product_scraper:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.mariadb_connection = mariadb.connect(user="s4dpython", password="s4dpython", database="producten")
        self.cursor = self.mariadb_connection.cursor()

    def __repr__(self):
        return "Scraper class voor : " + self.name

    def ah_scraper(self):
        for i in range(435427, 435437):
            product_suffix = "/wi" + str(i)
            temp_url = ah_url + product_suffix
            r = requests.get(temp_url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                element = soup.find("script", type="application/ld+json").text
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


albert_heijn = Product_scraper("Albert-Heijn", ah_url)

albert_heijn.ah_scraper()
