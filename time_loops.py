from datetime import datetime
import pytz
import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config
import configV
import math
from datetime import date 
from decimal import *
import os
import csv

def fonction1():
    
    global in_position
    in_position = True
    global last_price
    global TRADE_QUANTITY1
    global last_price2 
    last_price2 = -1
    TRADE_SYMBOL = 'FTMUSDT'
    last_price = 0
    tz_here = pytz.timezone("Asia/Macao")
    now= datetime.now(tz_here)
#timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    print(now)
    ticks = {}
    client = Client(config.API_KEY, config.API_SECRET)
    for filt in client.get_symbol_info(TRADE_SYMBOL)['filters']:
                if filt['filterType'] == 'LOT_SIZE':
                    step_size_reef= ticks['FTM'] = filt['stepSize']
                    step_size_usdt=ticks['USDT'] = filt['stepSize']
#print(step_size_reef)
#print(step_size_usdt)
    step_size_reef = float(step_size_reef)
    step_size_usdt = float(step_size_usdt)
    def get_usdt():
        try:
            balance = client.get_asset_balance(asset='USDT')
            print("M Balance Usdt {}" . format(balance))
        except Exception as e:
            return 0
        return balance['free']
    def test():   
        TRADE_QUANTITY1 = get_usdt()
        TRADE_QUANTITY1 = TRADE_QUANTITY1
        precision = int(round(-math.log(step_size_reef, 10), 0))
        TRADE_QUANTITY1 = round(float(TRADE_QUANTITY1), int(precision))
        order_succeeded = client.order_market_buy(symbol='FTMUSDT',quantity=float(TRADE_QUANTITY1))
        if order_succeeded:
            globals()['in_position'] = False
            #last_price = float(json_message['k']['l'])
            txt = order_succeeded
            last_price2 = txt
            globals()['last_price2'] = order_succeeded['fills'] 
            y = json.dumps(order_succeeded)
            fo = open('AchatEURM.json', 'w')
            data = json.load(y)
            for i in data['fills']:
                if i == i['price']:
                    fo.write(i['price'])
            fo.write(y)
            #fo.write(txt)
            fo.close()
    print(in_position)
    #print(last_price)
    print(last_price2)        

    test()
    
fonction1()