#!/usr/bin/python3
import sys
import math
from pycoingecko import api
class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

cg = api.CoinGeckoAPI()
if len(sys.argv) > 1:
    coin = sys.argv[1]
else:
    coin = "litecoin"
if len(sys.argv) > 2:
    base = 1 + int(sys.argv[2])/100
else:
    base = 1.05
price = cg.get_price(ids=coin, vs_currencies="btc")[coin]["btc"]
sprice =  '{:.8f}'.format(price)
print("COIN:", coin)
print("SPREAD-BASE:", base)
print()
print("Make 6 equally sized buckets of $BTC")
print(f"Buy {bcolors.OKGREEN}{coin}{bcolors.ENDC} at {bcolors.OKGREEN}{sprice}{bcolors.ENDC} with 3 of the six buckets.")
for bucket in range(0,6):
    pow1 = 2*bucket -6.5
    pow2 = 2*bucket -3.5
    price1 = '{:.8f}'.format(price*math.pow(base,pow1))
    price2 = '{:.8f}'.format(price*math.pow(base,pow2))
    if bucket < 3:
        print(f'Create buy order: {bcolors.OKGREEN}{price1}{bcolors.ENDC}, when filled, sell order at {price2}')
    else:
        print(f'Delay buy order for: {price1} untill sell order created now gets filled at {bcolors.OKGREEN}{price2}{bcolors.ENDC}')
