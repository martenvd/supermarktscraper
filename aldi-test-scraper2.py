import requests
from bs4 import BeautifulSoup
import json
import mysql.connector as mariadb

# TODO: producten naar database schrijven.
# TODO: ook het gewicht ophalen uit de html (deze staat niet in de dictionary).
# TODO: delay inbouwen na elke request om succes te garanderen.

class product_scraper:
    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.categories = self.get_aldi_categories()
        self.products = []

    def __repr__(self):
        return "Scraper class voor : " + self.name

    def get_aldi_categories(self):
        url = self.url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        soup.encode('UTF-8')
        temp_list = []
        for a in soup.find_all('a', href=True):
            if "/onze-producten/" in a['href']:
                temp_list.append(url + a['href'])
        temp_list = list(set(temp_list))
        return temp_list

    def get_aldi_product(self):
        for categorie in self.categories:
            categorie_url = categorie
            r = requests.get(categorie_url)
            soup = BeautifulSoup(r.text, "lxml")
            element = soup.find_all("script", type="application/ld+json")[-1].text
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
                    #print(productnaam, prijs, product_url, imagelink)
            except:
                pass


aldi = product_scraper("Aldi", "https://www.aldi.nl/")

aldi.get_aldi_product()
print(aldi.products)