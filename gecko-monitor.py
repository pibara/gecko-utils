#!/usr/bin/python3
from pycoingecko import api
from json import load
from time import sleep, time
from datetime import datetime
from pygame import mixer

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

with open("gecko-monitor.json") as jsonfile:
    data = load(jsonfile)

mixer.init()
alert=mixer.Sound('siren.wav')
last_alert = 0.0

holdings = data["holdings"]
currency = data["currency"]
allerts_low = data["allerts"]["low"]
allerts_high = data["allerts"]["high"]

cg = api.CoinGeckoAPI()
previous = dict()
for coin in holdings.keys():
    previous[coin] = None
previous["all"] = None
while True:
    total = 0.0
    start = time()
    for coin in holdings.keys():
        moment = str(datetime.now().time())[:5]
        holding = holdings[coin]
        price =  cg.get_price(ids=coin, vs_currencies=currency)
        if coin in allerts_low and price[coin][currency] < allerts_low[coin]:
            allert = allerts_low[coin]
            level = price[coin][currency]
            print(f"{bcolors.FAIL}{coin} LOW alert : {level}<{allert}{bcolors.ENDC}")
            if time() - last_alert > 60:
                last_alert = time()
                alert.play()
        if coin in allerts_high and price[coin][currency] > allerts_high[coin]:
            allert = allerts_high[coin]
            level = price[coin][currency]
            print(f"{bcolors.FAIL}{coin} HIGH alert: {level}>{allert}{bcolors.ENDC}")
            if time() - last_alert > 60:
                last_alert = time()
                alert.play()
        value = holding * price[coin][currency]
        if previous[coin] is not None:
            change = value - previous[coin]
            change = round(change*100)/100
            rounded = round(value*100)/100
            if change > 0.0:
                print(moment, "-", coin,"holding UP", change, "to", rounded)
            if change < 0.0:
                print(moment,"-", coin, "holding DOWN", -change, "to", rounded)
        total += value
        previous[coin] = value
    if previous["all"] is not None:
        change = total - previous["all"]
        change = round(change*100)/100
        if change > 0.0:
            # print(moment, "- TOTAL holdings up by", change)
            print(f"{bcolors.OKGREEN}{moment} - TOTAL holdings UP by {change}{bcolors.ENDC}")
        if change < 0.0:
            # print(moment,"- TOTAL holding down by", -change)
            mchange = -change
            print(f"{bcolors.WARNING}{moment} - TOTAL holdings DOWN by {mchange}{bcolors.ENDC}")
    previous["all"] = total
    rounded = round(100*total)/100
    moment = str(datetime.now().time())[:5]
    print(f"{bcolors.OKBLUE}{moment} {rounded}{bcolors.ENDC}")
    duration = time() - start
    remaining = 60 - duration
    if remaining > 0:
        sleep(remaining)
