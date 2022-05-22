import websocket ,json, pprint, numpy
from binance.client import Client
from binance.enums import *
import config
import math
from datetime import date 
from decimal import *
import os
# init
TRADE_SYMBOL = 'FTMUSDT'
TRADE_QUANTITY = '20'

client = Client(config.API_KEY, config.API_SECRET)
#client.API_URL = 'https://testnet.binance.vision/api'
# get balances for all assets & some account information
#print(client.get_account())
info = client.get_symbol_info('FTMUSDT')
print(info)
#print(info['filters'][2]['minQty'])

def order(symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order ...")
        order = client.create_order(symbol=symbol,side = side,type = order_type,quantity = quantity)
        print(order)
    except Exception as e:
        print(e)
        return False
    return True



print("VENTE de {}".format(TRADE_SYMBOL))

#order_succeeded = client.create_order(side=SIDE_SELL,type=ORDER_TYPE_MARKET,symbol='FTMUSDT',quantity=11)
trade_size = 11 # The trade size we want in USDT
sym = 'FTMUSDT' # the symbol we want to place a market order on
tick_size = 6 # the tick_size as per binance API docs
price = 19000 # Just making this up for now to exemplify, this is fetched within the script

trade_quantity = trade_size / price # Work out how much BTC to order
trade_quantity_str = "{:0.0{}f}".format(trade_quantity, tick_size)
symbol_info = client.get_symbol_info('FTMUSDT')
step_size = 0.0
for f in symbol_info['filters']:
  if f['filterType'] == 'LOT_SIZE':
    step_size = float(f['stepSize'])
precision = int(round(-math.log(step_size, 10), 0))

order1 = client.create_order(
    symbol='FTMUSDT',
    side='SELL',
    type=ORDER_TYPE_MARKET,
    #timeInForce=TIME_IN_FORCE_GTC,
    quantity=round(trade_size, precision))
    #price='0.60')

#symbol=TRADE_SYMBOL'',side=SIDE_SELL, type=ORDER_TYPE_MARKET,quantity=TRADE_QUANTITY)
print(order1)
#quan(self)

