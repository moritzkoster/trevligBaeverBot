import json
import random
import secrets
import requests
from bs4 import BeautifulSoup
from datetime import date

from telegram.ext import Updater, MessageHandler, Filters

with open('token.json', 'r') as token_file:
    token_dict = json.load(token_file)

updater = Updater(token=token_dict["token"], use_context=True)
dispatcher = updater.dispatcher

def message_handler(update, context):
    messageStr = update.message.text.lower().translate({ord(i): None for i in '.:;,?'})
    if messageStr == "isch de calmo en secco":
        context.bot.send_message(chat_id=update.message.chat_id, text="und wie!!! de allergrösst Secco")
    if messageStr == "isch de lano en secco":
        context.bot.send_message(chat_id=update.message.chat_id, text="nei uf kein Fall isch der Unseccoigschte überhaupt")
    message = update.message.text.lower().split()
    print(message)
    didSend = False
    if "zwiebel" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text="rostad lööööök!!!!")
        didSend = True
    if "arsch" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text="Jag äter din rostad röv")
        didSend = True
    if "biber" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text="treeevlig Bääver")
        didSend = True
    if "arschloch" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text="RÖV Loch!!!")
        didSend = True
    if "anker" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text=anker())
        didSend = True
    if "spar" in message and "lager" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text=spar_lager())
        didSend = True
    if "farmer" in message and not "naturtrüb" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text=farmer())
        didSend = True
    if "farmer" in message and "naturtrüb" in message:
        context.bot.send_message(chat_id=update.message.chat_id, text=farmer_Nat())
        didSend = True


def anker():
    promotion = 0
    if last["anker"]["date"] == date.today():
        promotion = last["anker"]["prom"]
    else:
        vgm_url = 'https://www.coop.ch/de/lebensmittel/getraenke/bier/multipacks-ab-12x50cl/anker-lager-bier-24x50cl/p/3458809'
        html_text = requests.get(vgm_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        promotion = soup.find(attrs={"data-testauto": "productlistpromotion3458809"}).get_text()
        last["anker"] = {"date": date.today(), "prom": promotion}

    if promotion == None:
        return "Keine Promotion"

    if "53%" in promotion:
        return "Anker halbe Priis!!!"
    else:
        return "Anker Aktion, aber nöd halbe Priis"


def spar_lager():

    promotion = 0
    if last["spar"]["date"] == date.today():
        prom = last["spar"]["prom"]
    # TODO: Name of Item
    else:
        item = "chopfab-draft-dose"
        url = "https://www.spar.ch/angebote/"

        r = requests.get(url + item)
        soup = BeautifulSoup(r.text, 'html.parser')
        prom = soup.find("span", attrs={"class": "m-item-teaser__icon-box__text-2 m-item-teaser__icon-box__text-2--alt"})
        last["spar"] = {"date": date.today(), "prom": prom}
    if not prom:
        return "Spar Lager isch gad ned Aktion :/"
    else:
        return "Spar-Lager isch Aktion: " + prom.get_text()

def farmer():
    promotion = 0
    farmerNorm = 9.0
    if last["farmer"]["date"] == date.today():
        price = last["farmer"]["price"]
    else:
        item = "lagerbier-farmer-dose-18-50-cl_26980"
        url = "https://www.landi.ch/shop/biere-mit-alkohol_200201/"

        r  = requests.get(url + item)
        soup = BeautifulSoup(r.text, 'html.parser')
        prom = soup.find("span", attrs={"class": "product-total-price"})
        price = float(prom.get_text())
        last["farmer"] = {"date": date.today(), "price": price}
    if price == farmerNorm:
        return "Farmerhülsen sind nicht Aktion"
    else:
        return f"Farmerhülsen sind Aktion: {100-price/farmerNorm*100}%, Wuuhuu"

def farmer_Nat():
    promotion = 0
    farmerNorm = 11.7
    if last["farmerNat"]["date"] == date.today():
        price = last["farmerNat"]["price"]
    else:
        item = "bier-farmer-naturtrueeb-dose-1850cl_38093"
        url = "https://www.landi.ch/shop/biere-mit-alkohol_200201/"

        r  = requests.get(url + item)
        soup = BeautifulSoup(r.text, 'html.parser')
        prom = soup.find("span", attrs={"class": "product-total-price"})
        price = float(prom.get_text())
        last["farmerNat"] = {"date": date.today(), "price": price}
    if price == farmerNorm:
        return "Farmerhülsen Naturtrüb sind nicht Aktion"
    else:
        return f"Farmerhülsen Naturtrüb sind Aktion: {100-price/farmerNorm*100}%, Wuuhuu"
#farmerNatTrübNorm = 11.7

last = {"anker": {"date": date(year=2021, month=4, day=28)},
        "spar": {"date": date(year=2021, month=4, day=28)},
        "farmer": {"date": date(year=2021, month=4, day=28)},
        "farmerNat": {"date": date(year=2021, month=4, day=28)}}

dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.start_polling()
