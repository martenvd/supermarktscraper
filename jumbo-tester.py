import requests
from bs4 import BeautifulSoup
import re

url = "https://www.jumbo.com/producten/?PageNumber=2"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
soup.encode('UTF-8')
prijs_list = []

for i in range(0,30,2):
    try:

        prijs = soup.find_all("span", class_="jum-price-format")[i].text
        prijs_list.append(prijs)
        print(int(prijs)/100)
    except:
        pass

