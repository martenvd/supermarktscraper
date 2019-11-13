from scraperclasses import *
import threading

aldi = Aldi_scraper()
jumbo = Jumbo_scraper()
coop = Coop_scraper()
albert_heijn = AH_scraper()

supermarkets = [aldi, jumbo, coop, albert_heijn]

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
