#!/usr/bin/env python3

import urllib.request
import json
import subprocess

with urllib.request.urlopen("https://api.coinmarketcap.com/v2/ticker/1027") as url:
    data = json.loads(url.read().decode())
    
    quotes = data["data"]["quotes"]["USD"]
    price = quotes["price"]
    percent_change_1h = quotes["percent_change_1h"]
    percent_change_24h = quotes["percent_change_24h"]
    percent_change_7d = quotes["percent_change_7d"]
    
    msg = "Price: {:.2f}$".format(price) + "\n" + \
          "\n" + \
          "1h:    {}%".format(percent_change_1h) + "\n" + \
          "24h:   {}%".format(percent_change_24h) + "\n" + \
          "7d:    {}%".format(percent_change_7d)
          
    subprocess.run(["/usr/bin/notify-send", "Ethereum Performance", msg])
