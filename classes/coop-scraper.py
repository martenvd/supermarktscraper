import requests
import json
from bs4 import BeautifulSoup
import mysql.connector as mariadb

class CoopParser():
    products = []

    def __init__(self):
        self.mariadb_connection = mariadb.connect(user="s4dpython", password="s4dpython", database="producten")
        self.cursor = self.mariadb_connection.cursor()
        self.fetch_all()

    def parse_page(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        soup.encode('UTF-8')
        return soup

    def fetch_categories(self):
        categories = []
        for link in self.parse_page('https://www.coop.nl/boodschappen/').find_all('a', href=True):
            if '/boodschappen/' in link['href']:
                categories.append(link['href'])
        categories = list(set(categories))
        return categories


    def fetch_products(self, category_url):
        page = self.parse_page(category_url + "?PageSize=99999")  # haal pagina met producten in categorie op
        for article in page.find_all('article'):  # loop over alle producten heen
            try:
                img = article.find('img')['data-srcset'].split()[0]  # afbeelding van product
                data = json.loads(article['data-product'])  # {"id":"3509","price":"1.69","list":"product-category","variant":"1 stuk(s)"}
                name = article.find('h2')['title']  # naam van product
                product_url = article.find('a')['href']
                hoeveelheid = data['variant']
                prijs = float(data['price'])
                product = {
                    'id': data['id'], #heeft ah dit ook?
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

                print("ik ben hier")
            except:
                pass


    def fetch_all(self):
        categories = self.fetch_categories() #haal cat pagina op en parse alle categorieen
        for cat in categories:
            self.fetch_products(cat) #haal alle producten van cateegorieen op

parser = CoopParser()
print(parser.products)