#!/usr/bin/env python3

from requests import Request, Session
import json
import subprocess
import sys
import configparser
import pathlib

config_path = str(pathlib.Path(__file__).parent.absolute()) + '/config.ini'
config = configparser.ConfigParser()
config.read(config_path)

MY_ETH = float(config["DEFAULT"]["MY_ETH"])
CRYPTOS = ['ETH', 'BTC']
FIATS = ['USD', 'EUR']
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config["DEFAULT"]["API_KEY"]
}

session = Session()
session.headers.update(HEADERS)

try:
    quotes = {}
    msg = ""
    for crypto in CRYPTOS:
        quotes[crypto] = {}
        for fiat in FIATS:
            params = {
                'symbol': crypto,
                'convert': fiat # only one fiat per request
            }
            response = session.get(URL, params=params)
            data = json.loads(response.text)
            quotes[crypto][fiat] = data["data"][crypto]["quote"][fiat]


        msg += "{}\n".format(crypto) + \
               "------------------------------\n" + \
               "Price: {:.2f}€\n".format(quotes[crypto]['EUR']["price"]) + \
               "Price: {:.2f}$\n".format(quotes[crypto]['USD']["price"]) + \
               "\n" + \
                "1h:    {}%\n".format(quotes[crypto]['USD']["percent_change_1h"]) + \
                "24h:   {}%\n".format(quotes[crypto]['USD']["percent_change_24h"]) + \
                "7d:    {}%\n\n".format(quotes[crypto]['USD']["percent_change_7d"])
    
    subprocess.run(["/usr/bin/notify-send", "Crypto Checker", msg])
except Exception as e:
    subprocess.run(["/usr/bin/notify-send", "Crypto Checker", str(e)])
