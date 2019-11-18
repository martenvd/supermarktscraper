from scraperclasses import *
import threading
import sys

aldi = Aldi_scraper()
jumbo = Jumbo_scraper()
coop = Coop_scraper()
albert_heijn = AH_scraper()

supermarkets = []

#Zonder argumenten worden alle supermarkten gescraped.
if len(sys.argv) < 2:
    supermarkets = [aldi, jumbo, coop, albert_heijn]
else:
    for argument in sys.argv:
        supermarkets.append(argument)
del supermarkets[0]

for index in range(len(supermarkets)):
    if supermarkets[index] == "aldi":
        supermarkets[index] = aldi
    elif supermarkets[index] == "jumbo":
        supermarkets[index] = jumbo
    elif supermarkets[index] == "albert_heijn":
        supermarkets[index] = albert_heijn
    elif supermarkets[index] == "coop":
        supermarkets[index] = coop
    else:
        print("[-] Invalid supermarket in arguments: {}".format(supermarkets[index]))

def start_scraper_thread(supermarket):
    print("[+] Starting scraper thread for {}".format(supermarket))
    supermarket.fetch_all_products()
    print("[*] Finished scraping for {}".format(supermarket))

if __name__ == "__main__":
    active_supermarkets = ""
    for supermarket in supermarkets:
        active_supermarkets += str(supermarket) + " | "
    print("[+] Preparing scrapers for: " + active_supermarkets)
    for supermarket in supermarkets:
        thread = threading.Thread(target=start_scraper_thread, args=(supermarket,))
        thread.start()
