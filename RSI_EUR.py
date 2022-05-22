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
RSI_PERIOD = 2

global RSI_OVERSOLD
global RSI_OVERBOUGHT
RSI_OVERBOUGHT = 78.3
RSI_OVERSOLD = 100
global TRADE_SYMBOL
TRADE_SYMBOL = 'FTMUSDT'
closes = []

global client
#global client2
#global TRADE_QUANTITY1
#global TRADE_QUANTITY2
#global TRADE_QUANTITY1V
#global TRADE_QUANTITY2V
global precision
global step_size_ftm              
global step_size_usdt             
ticks = {}

client = Client(config.API_KEY, config.API_SECRET)
client2 = Client(configV.API_KEY, configV.API_SECRET)
for filt in client.get_symbol_info(TRADE_SYMBOL)['filters']:
                if filt['filterType'] == 'LOT_SIZE':
                    step_size_ftm= ticks['FTM'] = filt['stepSize']
                    step_size_usdt=ticks['USDT'] = filt['stepSize']
#print(step_size_ftm)
#print(step_size_usdt)
step_size_ftm = float(step_size_ftm)
step_size_usdt = float(step_size_usdt)
def test():
        for f in json_message:
              if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
        precision = int(round(-math.log(step_size, 10), 0))
    
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
def get_usdt():
    try:
        balance = client.get_asset_balance(asset='USDT')
        print("M Balance Usdt {}" . format(balance))
    except Exception as e:
        return 0
    return balance['free']

def get_ftm():
    try:
        balance = client.get_asset_balance(asset='FTM')
        print("M Balance Ftm {}" . format(balance))
    except Exception as e:
        return 0
    return balance['free']
def status2():
    try:
        balance = client2.get_asset_balance(asset='USDT')
        print("V Balance Usdt {}" . format(balance))
        balance2 = client2.get_asset_balance(asset='FTM')
        print("V Balance Ftm {}" . format(balance2))
        TRADE_QUANTITY1 = float(balance['free'])
        TRADE_QUANTITY2 = float(balance2['free'])
    except Exception as e:
        return False
    return True
 

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order ...")
        order = client.create_order(
            symbol=symbol,
            side = side,
            type = order_type,
            quantity = quantity)
        print(order)
    except Exception as e:
        return False
    return True 
        
    
def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")
 

def on_message(ws,message):

    global closes
    global in_position
    in_position = True
    global TRADE_QUANTITY1
    global TRADE_QUANTITY2
    
    
    #global TRADE_QUANTITY1V
    #global TRADE_QUANTITY2V
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
            #print("tout les RSI jusqu'a present")
            #print(rsi)
            last_rsi = rsi[-1]
            print("les rsi actuel est {}". format(last_rsi))
            if (float(last_rsi) >= float(RSI_OVERBOUGHT)) and (float(last_price) < float(json_message['k']['l'])):
                if in_position:
                    TRADE_QUANTITY2 = get_ftm() 
                    precision = int(round(-math.log(step_size_ftm, 10), 0))
                    TRADE_QUANTITY2 = round(float(TRADE_QUANTITY2), int(precision))
                    order_succeeded = client.order_market_sell(symbol=TRADE_SYMBOL,quantity=float(TRADE_QUANTITY2))
                    #order_succeeded2 = order2(SIDE_SELL, TRADE_QUANTITY2V, "FTMUSDT")
                    in_position = False

                    if order_succeeded:
                        print("rsi :{}". format(last_rsi))
                        y = json.dumps(order_succeeded)
                        fo = open('VenteM.json', 'a')
                        fo.write(y)
                        fo.close()
                else:
                    print("OVERBOUGHT Vous n'en possedez aucun ")
            if last_rsi <= RSI_OVERSOLD :

                if in_position == True:
                    print("Over sold  on  {}  deja en  possession  ". format(TRADE_SYMBOL))
                else:  
                    TRADE_QUANTITY1 = get_usdt()
                    precision = int(round(-math.log(step_size_usdt, 10), 0))
                    print("Achat")
                    TRADE_QUANTITY1 = round(float(TRADE_QUANTITY1), int(precision))
                    order_succeeded = client.order_market_buy(symbol=TRADE_SYMBOL,quantity=float(TRADE_QUANTITY1))
                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY1, "FTMUSDT")
                    
                    if order_succeeded:
                        in_position = True
                        print("rsi :{}". format(last_rsi))
                        last_price = float(json_message['k']['l'])
                        y = json.dumps(order_succeeded)
                        fo = open('AchatM.json', 'a')
                        fo.write(y)
                        fo.close()
                        
                        
                    
status()
status2()
ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()



