import requests
from bs4 import BeautifulSoup
import lxml

ah_url = "http://www.ah.nl"
producten_suffix = "/producten"
producten_url = ah_url + producten_suffix

r = requests.get(producten_url)
soup = BeautifulSoup(r.text, 'lxml')
soup.encode('UTF-8')

producten_url_list = []

for a in soup.find_all('a', href=True):
    if "/producten/" in a['href'] and "/merk" not in a['href'] and "/eerder-gekocht" not in a['href']:
        producten_url_list.append(ah_url + a['href'])

producten_url_list = list(set(producten_url_list))

