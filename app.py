import logging
import pandas as pd
import re
import numpy as np
from numpy import random

#from telegram import Update, ForceReply
#from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import *
from telegram.ext import *
from telegram.ext import messagehandler
#Class
class find():
    def __init__(self, text):
        self.text = text
    def author(text):
        text = text.split('(')
        text = text[1].split(')')
        text = text[0]
        return text
    def book_name(text):
        text = text.split('(')
        text = text[0]
        return text
    def position(text):
        pattern = re.compile(r'[0-9]+-?[0-9]+')
        text = pattern.findall(text)[0]
        return text
    def day_of_week(text):
        pattern = re.compile(r': ([a-zA-Záç]+-?[a-z]+)')
        text = pattern.findall(text)[0]
        return text
    def date(text):
        pattern = re.compile(r'[0-9]+ [a-z]+ [a-z]+ [a-z]+ [0-9]+')
        text = pattern.findall(text)[0]
        return text
    def hour(text):
        pattern = re.compile(r'[0-9]+:[0-9]+:[0-9]+')
        text = pattern.findall(text)[0]
        return text
    def text(text):
        pattern = re.compile(r'[\S\s \n]+')
        text = pattern.findall(text)[0]
        return text     
#Read the document
with open('My Clippings.txt',"r",encoding='UTF-8') as arq:
    lines = arq.readlines()
    data = []
    cont  = 0
    highlight = 0
    for line in lines:
        if '=========' in lines[lines.index(line)-1]:
            author = find.author(line)
            book_name = find.book_name(line)
        if '=========' in lines[lines.index(line)-2]:
            position = find.position(line)
            day_of_week = find.day_of_week(line)
            date = find.date(line)
            hour = find.hour(line)
            if 'destaque' in line:
                type = 'Destaque'
            else:
                type = 'Nota'
        if '=========' in lines[lines.index(line)-4]:
            highlight = find.text(line)
        cont=cont+1
        if cont == 5:
            if highlight !=0:
                data.append([highlight,type,book_name,author,date,day_of_week,hour,position])
                highlight = 0
            cont = 0
              
df = pd.DataFrame(data,columns = ['Text','Type','Book','Author','Highlight date','Day of Week','Hour','Position'])


##Code from: https://github.com/python-telegram-bot/python-telegram-bot, adaptado
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    buttons = [[KeyboardButton('Frase Aleatória')]]
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        #reply_markup=ForceReply(selective=True),
        reply_markup=ReplyKeyboardMarkup(buttons),
    )
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def phrase(update: Update, context: CallbackContext) -> None:
    x = np.random.random_integers(0,142,size=1)
    for i in x:
        y = df.loc[[i],'Text'].values[0]
    update.message.reply_text(y)
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("Phrase", phrase))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text,phrase))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()