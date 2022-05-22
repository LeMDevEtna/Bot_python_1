import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config
import math
from datetime import date 
from decimal import *
import os
import csv



SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 77
RSI_OVERSOLD = 23.3
TRADE_SYMBOL = 'FTMUSD'
closes = []
last_price = 0
in_position  = True
global client
global TRADE_QUANTITY1
global TRADE_QUANTITY2

                     


client = Client(config.API_KEY, config.API_SECRET)

def status():
    try:
        balance = client.get_asset_balance(asset='USDT')
        balance2 = client.get_asset_balance(asset='FTM')
        TRADE_QUANTITY1 = float(balance['free'])
        TRADE_QUANTITY2 = float(balance2['free'])
    except Exception as e:
        return False
    return True
 

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order ...")
        order = client.create_order(symbol=symbol,side = side,type = order_type,quantity = quantity)
        print(order)
    except Exception as e:
        return False
    return True        
    
def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")
 

def on_message(ws,message):

    global tmp2
    global closes
    global walet
    global tmp2
    global commission 
    global commission2
    global ttc
    tmp2=0
    bought = 0
    print("received message --")
    
    json_message = json.loads(message)
    pprint.pprint(json_message['k']['l']) 
    #pprint.pprint(json_message )


    candle = json_message['k']
    is_candle_closed = candle['x']
    close  = candle['c']
    
    if is_candle_closed:

        print("Bougie fermé a {}".format(close))
        closes.append(float(close))
        print("fermetures")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            print("tout les RSI jusqu'a present")
            print(rsi)
            last_rsi = rsi[-1]
            print("les rsi actuel est {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT and last_price < json_message['k']['l']:
                if in_position:
                    status() 
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY2, TRADE_SYMBOL)

                if order_succeeded:
                    in_position = False
                    print("VENDRE {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                    with open('sales.json', 'a') as csv_file:
                        json.dump(order_succeeded, json_file)
                else:
                    print("OVERBOUGHT Vous n'en possedez aucun ")

            if last_rsi < RSI_OVERSOLD :

                if in_position:
                    print("Over sold  on  {}  deja en  possession  ".format(TRADE_SYMBOL))
                else:  
                    status()
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY1, TRADE_SYMBOL)

                if order_succeeded:
                    in_position = True
                    print("ACHETER  {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                    commission = commission + ((float(json_message['k']['l']) * 0.1) /100)
                    last_price = json_message['k']['l']
                    with open('sales.json', 'a') as csv_file:
                        json.dump(order_succeeded, json_file)
                        
                        
                    

ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()



