import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib3
import bs4
import requests
from bs4 import BeautifulSoup
import pandas as pd
from googlesearch import search
from telegram.ext import Updater, CommandHandler
import requests
import re
import logging



def UrlAction(nom_action):
    recherche=nom_action+"cours boursorama"
    a=search(recherche,1)
    #print(a)
    #print(type(a[0]))
    return(a[0])
#"https://www.boursorama.com/cours/1rPAI/")
def Valeur(url):
    r = requests.get(url)
#print (r.text)
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    #print(soup)
    span=soup.find("span", {"class": "c-instrument c-instrument--last"})
#soup.findAll("div", {"class": "c-faceplate__price "})
#print(help(BeautifulSoup.findAll))
    value=(span.string)

    span=soup.find("div", {"class": "c-instrument c-instrument--last"})
    name=soup.find("div", {"class": "u-text-bold"})
    #print(soup)
    print(name.string)
    return float(value)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    #print(type('update.message.text'))
    update.message.reply_text(Valeur(UrlAction(update.message.text)))



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1354114002:AAGCIUDlp7iDerVcmcxmaZikhrKhF9R1w4g", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
