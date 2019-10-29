import requests
from bs4 import BeautifulSoup
import json
import lxml
import re

ah_url = "https://www.ah.nl/producten/product"

prod_dict = {}

for i in range(435427,436427):
    product_suffix = "/wi" + str(i)
    temp_url = ah_url+product_suffix
    r = requests.get(temp_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        element = soup.find("script", type="application/ld+json").text
        element = json.loads(element)
        if 'offers' in element:
            print(element['offers']['price'])
