from requests import post, request
import telebot
from flask import Flask, request
import os
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


API_TOKEN  = '5526189505:AAGV3T6-SIgRa_mo1JrZsMkmdV5wjakklLM'

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start', 'botones'])
def send_welkome(message):
    bot.reply_to(message, "Hola, soy un ChatBot informativo de la Universidad Gran Asuncion")

# responde a los mensajes de texto que no son comandos
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.startswith("/"):
       bot.send_message(message.chat.id, "Hola, este comando no esta disponoble")
    else:
       bot.send_message(message.chat.id, "Hola, te recomiendo los siguientes comandos para consultar informacion y conocer un poco más acerca de la Universidad Gran Asunción") 


@bot.message_handler(commands=['botones'])
def cmd_botones(message):
    """Muestra un mensaje con botones inline (a continuacion del mensaje)"""
    markup = InlineKeyboardMarkup(row_width = 2)
    b1 = InlineKeyboardButton("UGA Radio", url="http://ugaradio.com.py/")
    b2 = InlineKeyboardButton("UNIGRAN WEB", url="https://www.unigran.edu.py/")
    b3 = InlineKeyboardButton("UNIGRAN FACEBOOK", url="https://www.facebook.com/unigranparaguay?_rdc=1&_rdr")
    markup.add(b1, b2, b3)
    bot.send_message(message.chat.id, "Enlaces que pueden intereasarte", reply_markup=markup)

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://bothimura.herokuapp.com/' + API_TOKEN)
    return "!", 200

if __name__ + '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))