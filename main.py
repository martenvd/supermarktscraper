from scraperclasses import *
import threading

aldi = Aldi_scraper()
jumbo = Jumbo_scraper()
coop = Coop_scraper()
albert_heijn = AH_scraper()

supermarkets = [aldi, jumbo, coop, albert_heijn]

def start_scraper_thread(supermarket):
    print("Starting scraper thread for {}".format(supermarket))
    supermarket.fetch_all_products()
    print("Finished scraping for {}".format(supermarket))

if __name__ == "__main__":
    threads = []
    for supermarket in supermarkets:
        thread = threading.Thread(target=start_scraper_thread, args=(supermarket,))
        threads.append(thread)
        thread.start()
