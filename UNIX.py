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



SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
global RSI_PERIOD
RSI_PERIOD = 14

global RSI_OVERSOLD
global RSI_OVERBOUGHT
RSI_OVERBOUGHT = 78.1
RSI_OVERSOLD = 23.9
TRADE_SYMBOL = 'FTMUSDT'
closes = []

global client
global client2
global TRADE_QUANTITY1
global TRADE_QUANTITY2
global TRADE_QUANTITY1V
global TRADE_QUANTITY2V

                     


client = Client(config.API_KEY, config.API_SECRET)
client2 = Client(configV.API_KEY, configV.API_SECRET)
def status():
    try:
        balance = client.get_asset_balance(asset='USDT')
        print("Balance Usdt {}" . format(balance))
        balance2 = client.get_asset_balance(asset='FTM')
        print("Balance Ftm {}" . format(balance2))
        TRADE_QUANTITY1 = float(balance['free'])
        TRADE_QUANTITY2 = float(balance2['free'])
    except Exception as e:
        return False
    return True

def status2():
    try:
        balance = client2.get_asset_balance(asset='USDT')
        print("Balance Usdt {}" . format(balance))
        balance2 = client2.get_asset_balance(asset='FTM')
        print("Balance Ftm {}" . format(balance2))
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

def order2(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order ...")
        order = client2.create_order(symbol=symbol,side = side,type = order_type,quantity = quantity)
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
    global in_position
    in_position = True
    tmp2=0
    bought = 0
    global last_price 
    last_price = float(0.60)
    print("received message --")
    
    json_message = json.loads(message)
    pprint.pprint(json_message['k']['l']) 
    #pprint.pprint(json_message )


    candle = json_message['k']
    is_candle_closed = candle['x']
    close  = candle['c']
        
    if is_candle_closed:

        print("Bougie fermé a {}". format(close))
        closes.append(float(close))
        print("fermetures")
        #print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            print("tout les RSI jusqu'a present")
            #print(rsi)
            last_rsi = rsi[-1]
            print("les rsi actuel est {}". format(last_rsi))
            if (float(last_rsi) >= float(RSI_OVERBOUGHT)) and (float(last_price) < float(json_message['k']['l'])):
                print("attention 1")
                if in_position:
                    status()
                    status2() 
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY2, "FTMUSDT")
                    order_succeeded2 = order2(SIDE_SELL, TRADE_QUANTITY2V, "FTMUSDT")
                    in_position = False

                    if order_succeeded:
                        print("rsi :{}". format(last_rsi))
                        with open('salesM.json', 'w') as csv_file:
                            json.dump(order_succeeded, json_file)
                else:
                    print("OVERBOUGHT Vous n'en possedez aucun ")
            if last_rsi <= RSI_OVERSOLD :

                if in_position == True:
                    print("Over sold  on  {}  deja en  possession  ". format(TRADE_SYMBOL))
                else:  
                    status()
                    status2()
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY1, "FTMUSDT")
                    order_succeeded2 = order2(SIDE_BUY, TRADE_QUANTITY1V, "FTMUSDT")
                    
                    if order_succeeded:
                        in_position = True
                        print("rsi :{}". format(last_rsi))
                        #commission = commission + ((float(json_message['k']['l']) * 0.1) /100)
                        last_price = float(json_message['k']['l'])
                        with open('sales.json', 'a') as csv_file:
                            json.dump(order_succeeded, json_file)
                        
                        
                    
status()
status2()
ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()



