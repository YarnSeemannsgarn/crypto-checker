#!/usr/bin/env python3

import urllib.request
import json
import subprocess

ETHEREUM = 13.217855

cryptos = [(1027, "Ethereum"), (1, "Bitcoin")]

msg = ""
for crypto in cryptos:
    with urllib.request.urlopen("https://api.coinmarketcap.com/v2/ticker/{}".format(crypto[0])) as url:
        data = json.loads(url.read().decode())
        quotes = data["data"]["quotes"]["USD"]
        msg += "{}\n".format(crypto[1]) + \
               "------------------------------\n" + \
               "Price: {:.2f}$\n".format(quotes["price"]) + \
               "\n" + \
               ("Total: {:.2f}$\n".format(float(quotes["price"]) * ETHEREUM) if crypto[1] == "Ethereum" else "") + \
               "1h:    {}%\n".format(quotes["percent_change_1h"]) + \
               "24h:   {}%\n".format(quotes["percent_change_24h"]) + \
               "7d:    {}%\n\n".format(quotes["percent_change_7d"])
    
subprocess.run(["/usr/bin/notify-send", "Crypto Checker", msg])
