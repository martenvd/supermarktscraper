# python scraper
import requests
from bs4 import BeautifulSoup

# python telegram bot
import telegram
import logging
from telegram.ext import CommandHandler
from telegram.ext import Updater

# rest libraries
from random import randint

updater = Updater(token='695976918:AAEV9pbE0wXwc1rVazROFP9XEDN9bEO9eWc', use_context=True)
bot = telegram.Bot(token='695976918:AAEV9pbE0wXwc1rVazROFP9XEDN9bEO9eWc')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def wtf(update, context):
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('whatshappening.mp3', 'rb'))


def scrape(update, context):
    if "http" in context.args[0]:
        page = requests.get(context.args[0])
    else:
        page = requests.get("http://" + context.args[0])

    soup = BeautifulSoup(page.content, features="lxml")
    links = soup.find_all('a')
    scrape_response = ""
    blank_page = True
    link_list = []

    for link in links:
        string_link = str(link.get("href"))
        if "http" in string_link:
            link_list.append(string_link)
            if len(link_list) < 20:
                scrape_response += (str(link) + "\n")
                blank_page = False
            else:
                scrape_response = "Too many <a> elements on the page, sorry"
                blank_page = False

    if blank_page:
        scrape_response = "No http element found"

    context.bot.send_message(chat_id=update.effective_chat.id, text=scrape_response)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def parrot(update, context):
    parrot_img = 'https://media1.tenor.com/images/f8d3bb744832ecb22702ab5ca70bcd1b/tenor.gif'
    context.bot.send_animation(chat_id=update.effective_chat.id, animation=parrot_img)


def random_number(update, context):
    random_num = randint(0, 10)
    context.bot.send_message(chat_id=update.effective_chat.id, text=random_num)


handlers = [CommandHandler('start', start),
            CommandHandler('parrot', parrot),
            CommandHandler('num', random_number),
            CommandHandler('scrape', scrape, pass_args=True),
            CommandHandler('wtf', wtf)]

for i in range(0, (len(handlers)-1)):
    dispatcher.add_handler(handlers[i])

updater.start_polling()
