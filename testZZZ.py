import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv
import os
import cconfig
from datetime import datetime

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_5m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 79
RSI_OVERSOLD = 19
TRADE_SYMBOL = 'FTMUSD'
TRADE_QUANTITY = 25
closes = []
last_price = 0
in_position  = False
tmp = 0
waletAvant = 1000
coco = 0

#csvfile = open('RSITESTFinal.txt', 'w', newline='')
#candlestick_writer = csv.writer(csvfile, delimiter=',')
# si data coherente avec data binance lance ordre limite au prix tmp et lancer serv 
#V2 faire interface pouir les variables


client = Client(cconfig.KEY1, cconfig.KEY2, tld='us')
candlesticks = client.get_historical_klines(cconfig.SYMBOL, Client.KLINE_INTERVAL_1MINUTE, "1 JAN , 2021", "29 OCT, 2021")
walet = 1000
start = 0
end = 0
BENEFICE = 0
closes = []
bought = 0
ttCom = 0
nombreAction = 0 
def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")

def pourcentage_augment(start, end):
    pourcentage = ((float(end)) / float(start)-1)*100
    print(pourcentage)
    return (pourcentage)


def convertA(tab):
    arr = []
    for i in tab:
        arr.append(float(i[4]))
    arr = numpy.array(arr)
    return (arr)

#L'index de Candlesticks est mauvais j'ai l'impression, regarde les print
#Genre le premier buy, le RSI est à 19 et le BTC coûte 61k, soit la plus
#haute valeur de tout les buy, vérifez les walet
def on_message():
    global closes
    global walet
    global tmp
    global BENEFICE
    global ttCom
    global bought
    global nombreAction
    mdr = 0
    ttCom =0
    global coco
    global waletAvant

    print("received message --")

    if len(candlesticks) > RSI_PERIOD:
        np_closes = numpy.array(candlesticks)
        np_closes = convertA(np_closes)
        print(np_closes)
        rsi = talib.RSI(np_closes,14)
        print(rsi)
        print("tout les RSI jusqu'a present")
        #print(rsi)
        last_rsi = rsi[-1]
        print("les rsi actuel est {}".format(last_rsi))

        for i in range(len(rsi)):
            unix = candlesticks[i][0]/1000.0
            if rsi[i] < 28.2 and bought == 0:
                tmp = candlesticks[i][4]
                commisionAchat = (walet*0.001)
                bought = 1
                fichier = open("data.txt", "a")
                fichier.write("\n BUY I = " + str(i) + " | TMP = " + str(tmp) + " | RSI  = " + str(rsi[i])+ " | RSI + 1  = " + str(rsi[i+1])+ " | time  = " + str(datetime.fromtimestamp(
                unix)) + "com "+str(commisionAchat) + "ttcom : " +str(ttCom))
                fichier.close()
                print("BUY I = " + str(i) + " | TMP = " + str(tmp) + " | RSI  = " + str(rsi[i])+ " | RSI + 1  = " + str(rsi[i+1])+ " | time  = " + str(datetime.fromtimestamp(
                unix)) + " com "+str(commisionAchat) + " ttcom : " +str(ttCom))
                nombreAction  = float(walet)/float(tmp)
                walet  -= commisionAchat
                BENEFICE-=commisionAchat
                ttCom+= commisionAchat
                print( "avec walet "+str(walet)+ " NOMBRE d ACTION = "+str(nombreAction))
                
                
            if rsi[i] > 61.8 and float(candlesticks[i][4]) > (float(tmp) + float(tmp) * 0.06)   and float(tmp) != 0 and bought == 1:
                bought = 0
                print("SELL I = " + str(i) + " | TMP = " + str(tmp) + " | REAL PRICE = " + str(candlesticks[i][4]) + " | RSI  = " + str(rsi[i])+ " | RSI  + 1 = " + str(rsi[i+1])+ " | time  = " + str(datetime.fromtimestamp(
                unix)))
                fichier = open("data.txt", "a")
                fichier.write("\n SELL I = " + str(i) + " | TMP = " + str(tmp) + " | REAL PRICE = " + str(candlesticks[i][4]) + " | RSI  = " + str(rsi[i])+ " | RSI  + 1 = " + str(rsi[i+1])+ " | time  = " + str(datetime.fromtimestamp(
                unix)))
                fichier.close()
                

                BENEFICE +=  ((walet * (pourcentage_augment(tmp, candlesticks[i][4])/100))) 
                waletAvant += ((walet * (pourcentage_augment(tmp, candlesticks[i][4])/100)))
                walet += ((walet * (pourcentage_augment(tmp, candlesticks[i][4])/100)))
                
                ttCom += (walet * 0.001) 
                commissionVente = (walet * 0.001)
                BENEFICE -= (walet * 0.001) 
                walet -= commissionVente
                
                
                print( "BENEFICE "+ str(BENEFICE) + "WALET "+str(walet) + " commission achat + vente " +str(ttCom))

on_message()
if bought == 1:
    print("Position = " + str(bought) )
    print("Evolution brut depuis capital (1000) du Wallet initial  = " + str(waletAvant) )
    print("Action = " + str(nombreAction) )
    print("Valeur Walet au derniere achat  = " + str(walet))
    print("Benefice = " + str(BENEFICE ))
    print("CommissionTT = " + str(ttCom))
else:    
    print(" Walet = " + str(walet))
    print("Benefice = " + str(BENEFICE))
    print("CommissionTT = " + str(ttCom))
#ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
#ws.run_forever()
#outF.close()