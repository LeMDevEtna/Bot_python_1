from datetime import datetime
#import requests

import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 20
TRADE_SYMBOL = 'FTMUSD'
TRADE_QUANTITY = 25
closes = []
in_position  = False
client = Client(config.API_KEY, config.API_SECRET)
#req = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
#print(req)
req = client.get_avg_price(symbol="FTMUSDT")
prices = client.get_all_tickers()

print(req)

print(prices)

#now = datetime.now()
#var = True
#while (var):
#	if now.minute == 23 and now.second == 0 :
#		print (now.microsecond)
#		var = False
#	now = datetime.now()	
	#print (now.day)
	#print (now.hour)
	#print (now.minute)
	#print (now.second)
	