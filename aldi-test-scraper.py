import requests
from bs4 import BeautifulSoup
import json
import mysql.connector as mariadb

aldi_url = "https://www.aldi.nl"

# Categorien ophalen en in een list stoppen.
r = requests.get(aldi_url)
soup = BeautifulSoup(r.text, 'lxml')
soup.encode('UTF-8')

categorie_url_list = []

for a in soup.find_all('a', href=True):
    if "/onze-producten/" in a['href']:
        categorie_url_list.append(aldi_url + a['href'])

categorie_url_list = list(set(categorie_url_list))

# Producten ophalen per categorie en printen.
# TODO: producten naar database schrijven.
# TODO: ook het gewicht ophalen uit de html (deze staat niet in de dictionary).
# TODO: delay inbouwen na elke request om succes te garanderen.
for categorie in categorie_url_list:
    categorie_url = categorie
    r = requests.get(categorie_url)
    soup = BeautifulSoup(r.text, "lxml")
    # De laatste match van de soup.find_all is onze producten dictionary.
    element = soup.find_all("script", type="application/ld+json")[-1].text
    element = json.loads(element)
    # Try and Except omdat er soms iets mis gaat, dan moet de scrape wel doorgaan.
    try:
        num_items = element['numberOfItems']
        for i in range(0, num_items):
            productnaam = element['itemListElement'][i]['name']
            prijs = element['itemListElement'][i]['offers']['price']
            product_url = element['itemListElement'][i]['url']
            imagelink = element['itemListElement'][i]['image']
            print(productnaam, prijs, product_url, imagelink)
    except:
        pass
