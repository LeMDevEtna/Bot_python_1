import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config
import math
from datetime import date 
from decimal import *
import os
import csv
import configV
SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 77
RSI_OVERSOLD = 23.3
TRADE_SYMBOL = 'FTMUSD'
#TRADE_QUANTITY = 25
closes = []
last_price = 0
in_position  = True
global client
global client2
global TRADE_QUANTITY1
global TRADE_QUANTITY2
global TRADE_QUANTITY1V
global TRADE_QUANTITY2V
#csvfile = open('RSITESTFinal.txt', 'w', newline='') 
#candlestick_writer = csv.writer(csvfile, delimiter=',')
                     


client = Client(config.API_KEY, config.API_SECRET)
client2 = Client(configV.API_KEY, configV.API_SECRET)

def statusA():
    try:
        balance = client.get_asset_balance(asset='USDT')
        balance2 = client.get_asset_balance(asset='FTM')
        TRADE_QUANTITY1 = float(balance['free'])
        TRADE_QUANTITY2 = float(balance2['free'])
    except Exception as e:
        return False
    return True

def leSt():
    try:
        balance = client.get_asset_balance(asset='USDT')
        balance2 = client.get_asset_balance(asset='FTM')
    except Exception as e:
        raise e


def status2():
    balance = client2.get_asset_balance(asset='USDT')
    balance2 = client2.get_asset_balance(asset='FTM')
    TRADE_QUANTITY1V = float(balance['free'])
    TRADE_QUANTITY2V = float(balance2['free'])    

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
    global closes
    print("received message --")
    
    json_message = json.loads(message)
    pprint.pprint(json_message['k']['l']) 
   # pprint.pprint(json_message )      
    
    candle = json_message['k']
    is_candle_closed = candle['x']
    close  = candle['c']
    
    if is_candle_closed:
        print("Bougie fermé a {}".format(close))
        closes.append(float(close))
        print("fermetures")
        #print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            print("tout les RSI jusqu'a present")
            print(rsi)
            last_rsi = rsi[-1]
            print("les rsi actuel est {}".format(last_rsi))
            
            if last_rsi > RSI_OVERBOUGHT and last_price < json_message['k']['l']:
                #if in_position:
                print("VENDREEEEEEE {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                outF = open("MomoTest1.txt",'w')
                outF.write(" vendu  à :")
                outF.write(json_message['k']['l'])
                outF.close() 
                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                    #    in_position = False
                #else:
                    #print("OVERBOUGHT Vous n'en possedez aucun ")            
            if last_rsi < RSI_OVERSOLD:
                #if in_position:
                    #print("Over sold  on  {}  but you own it ".format(TRADE_SYMBOL))
                #else:  
                print("ACHETER !!! {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                outF = open("MomoTest1.txt",'w')
                last_price = json_message['k']['l']
                outF.write(" acheter  à :")
                outF.write(json_message['k']['l'])
                outF.close()     
                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                        #in_position = True

def on_message2(ws,message):

    global tmp2
    global closes
    global walet
    global tmp2
    global commission 
    global commission2
    global ttc
    global TRADE_QUANTITY1
    global TRADE_QUANTITY2
    global TRADE_QUANTITY1V
    global TRADE_QUANTITY2V
    tmp2=0
    bought = 0
    statusA()
    status2()
    print("received message --")
    
    json_message = json.loads(message)
    pprint.pprint(json_message['k']['l']) 
    pprint.pprint(json_message )


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
                    statusA()
                    status2() 
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY2, TRADE_SYMBOL)
                    order_succeeded2 = order2(SIDE_SELL, TRADE_QUANTITY2V, TRADE_SYMBOL)

                if order_succeeded:

                    in_position = False
                    print("VENDRE {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                    #outF = open("Resultat_Bot_Fil_Rouge.txt",'a')
                    #outF.write(" vendu  à : {} \n" . str(json_message['k']['l']))
                    #outF.write(" bill   : {} \n" . str(order_succeeded))
                    commission2  = commission2 + ((float(json_message['k']['l']) * 0.1) /100)
                    #outF.write("  commissionVentePredi  : {} \n" . str(commission2))
                    #outF.close()
                    with open('sales.json', 'a') as csv_file:
                        json.dump(order_succeeded, json_file)
                else:

                    print("OVERBOUGHT Vous n'en possedez aucun ")            
            if last_rsi < RSI_OVERSOLD :

                if in_position:
                    print("Over sold  on  {}  deja en  possession  ".format(TRADE_SYMBOL))
                else:  
                    status()
                    status2() 
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY1, TRADE_SYMBOL)
                    order_succeeded2 = order2(SIDE_BUY, TRADE_QUANTITY1V, TRADE_SYMBOL)

                if order_succeeded:

                    in_position = True
                    print("ACHETER  {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                    commission = commission + ((float(json_message['k']['l']) * 0.1) /100)
                    #outF = open("Resultat_Bot_Fil_Rouge.txt",'a')
                    last_price = json_message['k']['l']
                    #outF.write(" acheter  à : {} \n" . str(json_message['k']['l']))
                    #outF.write(" bill   : {} \n" . str(order_succeeded))
                    #outF.write("  commissionAchatPredi  : {} \n" . str(commission2))
                    #outF.close()
                    with open('sales.json', 'a') as csv_file:
                        json.dump(order_succeeded, json_file)
                        
                        
                    

ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message2)
ws.run_forever()

# init
TRADE_SYMBOL = 'FTMUSDT'
TRADE_QUANTITY = '29,2'
client = Client(config.API_KEY, config.API_SECRET)
info = client.get_symbol_info('FTMUSDT') 
info2 = client.get_margin_asset(asset='BNB')
balance = client.get_asset_balance(asset='USDT')
print(balance['free'])           
test = 2


