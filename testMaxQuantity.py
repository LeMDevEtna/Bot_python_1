import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config,csv
import os

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 79
RSI_OVERSOLD = 19
TRADE_SYMBOL = 'FTMUSD'
TRADE_QUANTITY = 25
closes = []
last_price = 0
in_position  = False
outF = open("MomoTest1.txt",'a')

client = Client(config.API_KEY, config.API_SECRET, tld='us')

info = client.get_symbol_info('BNBBTC')



#info = client.get_margin_asset(asset='BNB')

pprint(info)
