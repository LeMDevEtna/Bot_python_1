import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv
import os
import pandas as pd
from datetime import datetime
##
##Evolution regarder le benefice si benefice encore positif si perte superieur a 5 % pendant 2 jours conséqutif vendre a prete de benefice uniquement   pendant chute de tendance alors attendre le prochain point ba  pour reprendre la strategie
##

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 77
RSI_OVERSOLD = 25
TRADE_SYMBOL = 'FTMUSDT'
TRADE_QUANTITY = 21
closes = []
last_price = 0
in_position  = False
tmp = 0
global ttc
ttc = 0


#csvfile = open('RSITESTFinal.txt', 'w', newline='')
#candlestick_writer = csv.writer(csvfile, delimiter=',')

rsi_ACHAT = 23.3
rsi_VENTE = 77
client = Client('ZO4DljUT8x1BuqtNGk29oW1EayLQo3ai2Z8pT9Af4DtsZ9K2fzf1jJsIMLcASTnX', 'g0XId9rEs0A7zCYV4Dd2Xs5zJZN1LAGWwvxO5UT2fd9xXZY88G2iV05rdLhRsyPB', tld='us')
candlesticks = client.get_historical_klines('YFIUSDT', Client.KLINE_INTERVAL_1MINUTE, "1 OCT, 2021")#, "24 JUL, 2020"
wallet = last_price
start = 1000
end = 0
closes = []
BENEFICE = 0
EmergencyLostLimit = 5 #(percent)
#print(candlesticks[][])
#
#
#
# A FAIRE  VERIFICATION  BOT  VERIF ACHAT ET VENTE !! 
#
#


def addBenef(quantity):
    BENEFICE += quantity
     
def EmergencyExit():
    #set une 
    #if Wallet ==
    return  ok
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order ...")
        #order = client.create_order(symbol=symbol,side = side,type = order_type,quantity = quantity)
        #print(order)
    except Exception as e:
        return False
    return True

def orderLimit(side, quantity, symbol, order_type=ORDER_TYPE_LIMIT):
    try:
        print("sending order ...")
        #order = client.create_order(symbol=symbol,side = side,type = order_type,quantity = quantity)
        #print(order)
    except Exception as e:
        return False
    return True     
def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")

def pourcentage_augment(start, end):
    pourcentage = (float(end) - float(start)) / float(start)
    return (pourcentage)

def movingAverage(values,length):
    taille = numpy.repeat(1.0,length)/ length
    smas = numpy.convolve(values,taille,'Valid')
    return smas

def convertA(tab):
    arr = []
    for i in tab:
        arr.append(float(i[4]))
    arr = numpy.array(arr)
    return (arr)

def percent(part,whole):
    return 100 * float(part)/float(whole)

def on_message():
    
    closes =[]
    walet = 1000
    tmp2 = 0
    commission = 0
    commission2 = 0
    ttc = 0
    tmp2=0
    tmp=0
    global BENEFICE
    global start
    bought = 0
    mdr = 0
    values = []
    print("received message --")
    secu = False
    waletDepart = 1000

    if len(candlesticks) > 14:
        
        np_closes = numpy.array(candlesticks)
        np_closes = convertA(np_closes)
        #print(np_closes)
        rsi = talib.RSI(np_closes)
        print("tout les RSI jusqu'a present")

        last_rsi = rsi[0]
        print("les rsi actuel est {}".format(last_rsi))
        commission = 0
        commission2 = 0
        for i in range(len(rsi)):
            if BENEFICE > (0.1*waletDepart):
                secu = True
            values.append(float(candlesticks[i][4]))
            if rsi[i] < 28.2 and bought == 0:
                tmp2 = float(candlesticks[i][4])
                commission = commission + ((walet/100)*0.1)
                tmp  = tmp2 #- ((tmp2 * 0.1)/100)

                bought = 1
                unix = candlesticks[i][0]/1000.0
                print("BUY | price = " + str(tmp) + " | RSI  = " + str(rsi[i])+"| sma : "+str(movingAverage(values,9)[-1])+ " | time  = " + str(datetime.fromtimestamp(
                unix)))
                
            if rsi[i] > 81.3 and float(candlesticks[i][4]) > float(tmp) + 0.05*float(tmp) and float(tmp) != 0 and bought == 1   :
                unix = candlesticks[i][0]/1000.0
                commission2  = commission2 + ((walet / 100) *0.1)
                
                #print("ACHETER !!! {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                bought = 0
                print("SELL I = " + str(i) + " | TMP = " + str(tmp2) +"| sma : "+str(movingAverage(values,9)[-1])+ " | REAL PRICE = " + str(candlesticks[i][4]) +  " |  Benefice = " + str(BENEFICE)+ " | RSI  = " + str(rsi[i])+ " | time  = " + str(datetime.fromtimestamp(
                unix)))
                
                #print(str(movingAverage(values[:i+1],9)))
                print("percent " +str(walet * pourcentage_augment(tmp, candlesticks[i][4])))
                BENEFICE = BENEFICE + (walet * pourcentage_augment(tmp, candlesticks[i][4])) 
                walet = (walet * pourcentage_augment(tmp, candlesticks[i][4])) + walet
                
               
                #walet = (walet * pourcentage_augment(tmp, candlesticks[i][4])) + walet
            #i += 14
            #ttc = int(commission) + int(commission2)
    ttc = ttc + int(commission2) 
    print("Secure : "+ str(secu))        
    print("Walet = " + str(walet))
    print("commission = " + str(ttc))
    
    res = int(walet)-int(ttc)
    
    print("Walet - commission = " + str(res))
#val = percent(0.10,1000)
#print(str(val))  
on_message()
#print("Walet = " + str(walet))
#ttCom = int(commission) + int(commission2)
#print("commission = " + str(ttc))
#res = int(walet)-int(ttc)
#print("Walet - commission = " + str(res))
#print("rsi Achat = "+str(rsi_ACHAT)+" rsi Vente = "+str(rsi_VENTE))
#ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
#ws.run_forever()
#outF.close()