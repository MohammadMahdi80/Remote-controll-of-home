import requests
import numpy as np
import urllib.request
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters

from telegram import GameHighScore, Update 
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from telegram.chataction import ChatAction

import iot_database as db
import iot_database


token = "1835281848:AAFkk24Tz0SbBucDyM12w4_w09ntMYqYSkI"
lamp = 0
t_lamp = 0
wait_msg = 0

with open('./a.txt','r') as f:
    PASSWORD = f.readline()

def start_handler(update: Update, context: CallbackContext):
    ReplyKeyboardRemove()
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    global PASSWORD
    with open('./a.txt','r') as f:
        PASSWORD = f.readline()

    global lamp
    msg=requests.get("https://api.thingspeak.com/channels/1825423/fields/1.json?api_key=S4UIM4O8ZWOXQ2A8&results=2")
    lamp=int(msg.json()['feeds'][-1]['field1'])

    if not db.search(chat_id=chat_id):
        db.insert(chat_id,'start', 0, 0, 0, 0, 99, 'motor:off:0')
    else:
        db.update('start', chat_id)
    

    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    context.bot.sendMessage(chat_id, f'⚜️ Hello {first_name}\n\n🔐 Please Enter password:', reply_markup=ReplyKeyboardRemove())



def text_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text
    message_id = update.message.message_id
    pos = db.search(chat_id=chat_id)[0][1]

    global lamp
    global t_lamp
    global wait_msg
    msg=requests.get("https://api.thingspeak.com/channels/1825423/fields/1.json?api_key=S4UIM4O8ZWOXQ2A8&results=2")
    lamp=int(msg.json()['feeds'][-1]['field1'])

    if pos == 'start':
        if str(text) == str(PASSWORD):
            main_menu_handler(update, context)
        else:
            ReplyKeyboardRemove()
            context.bot.sendMessage(chat_id, "❌Wrong password!\n\n♻️Try again.",reply_markup=ReplyKeyboardRemove())
 
    if text == "🔴 Turn off lamp":
        if time.time() - t_lamp < 15:
            buttons = [["🔴 Turn off lamp"]]
            if wait_msg == 0:
                context.bot.sendMessage(chat_id, f'⏳please Wait {np.abs(15 - int(time.time() - t_lamp))} second and try later!')
                wait_msg = message_id + 1
            else:
                context.bot.editMessageText(f'⏳please Wait {np.abs(15 - int(time.time() - t_lamp))} second and try later!',chat_id,wait_msg)
                context.bot.delete_message(chat_id, message_id )
        else:
            urllib.request.urlopen('https://api.thingspeak.com/update?api_key=6D2G6KX0C85J75O9&field1='+"0")
            buttons = [["🟢 Turn on lamp"]]
            context.bot.sendMessage(chat_id, f'✅ Successfully Done!', 
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
            t_lamp = time.time()
            wait_msg = 0
    if text == "🟢 Turn on lamp":
        if time.time() - t_lamp < 15:
            buttons = [["🟢 Turn on lamp"]]
            if wait_msg == 0:
                context.bot.sendMessage(chat_id, f'⏳please Wait {np.abs(15 - int(time.time() - t_lamp))} second and try later!')
                wait_msg = message_id + 1
            else:
                context.bot.editMessageText(f'⏳please Wait {np.abs(15 - int(time.time() - t_lamp))} second and try later!',chat_id,wait_msg)
                context.bot.delete_message(chat_id, message_id )
        else:
            urllib.request.urlopen('https://api.thingspeak.com/update?api_key=6D2G6KX0C85J75O9&field1='+"1")
            buttons = [["🔴 Turn off lamp"]]
            context.bot.sendMessage(chat_id, f'✅ Successfully Done!', 
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
            t_lamp = time.time()
            wait_msg = 0



def main_menu_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    db.update('main_menu_handler', chat_id)
    global lamp
    if lamp == 1:
        buttons = [["🔴 Turn off lamp"]]
    else:
        buttons = [["🟢 Turn on lamp"]]
    context.bot.sendMessage(chat_id, f'✅ welcome to IOT bot!', 
    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


updater = Updater(token, use_context=True)

updater.dispatcher.add_handler(CommandHandler("start", start_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
updater.start_polling()






# msg=str(0)
# b=urllib.request.urlopen('https://api.thingspeak.com/update?api_key=6D2G6KX0C85J75O9&field1='+msg)
# time.sleep(16)
# b=urllib.request.urlopen('https://api.thingspeak.com/update?api_key=6D2G6KX0C85J75O9&field1='+"0")
