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
CRYPTOS =  ["ETH", "BTC"]
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config["DEFAULT"]["API_KEY"]
}

session = Session()
session.headers.update(HEADERS)

try:
    msg = ""
    for crypto in CRYPTOS:
        parameters = {
            'symbol': crypto
        }
        response = session.get(URL, params=parameters)
        data = json.loads(response.text)
        quotes = data["data"][crypto]["quote"]["USD"]
        msg += "{}\n".format(crypto) + \
               "------------------------------\n" + \
               "Price: {:.2f}$\n".format(quotes["price"]) + \
               "\n" + \
               ("Total: {:.2f}$\n".format(float(quotes["price"]) * MY_ETH) if crypto == "ETH" else "") + \
               "1h:    {}%\n".format(quotes["percent_change_1h"]) + \
               "24h:   {}%\n".format(quotes["percent_change_24h"]) + \
               "7d:    {}%\n\n".format(quotes["percent_change_7d"])
    
    subprocess.run(["/usr/bin/notify-send", "Crypto Checker", msg])
except Exception as e:
    subprocess.run(["/usr/bin/notify-send", "Crypto Checker", str(e)])
