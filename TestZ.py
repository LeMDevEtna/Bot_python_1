import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv
import os

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

#csvfile = open('RSITESTFinal.txt', 'w', newline='')
#candlestick_writer = csv.writer(csvfile, delimiter=',')


client = Client('ZO4DljUT8x1BuqtNGk29oW1EayLQo3ai2Z8pT9Af4DtsZ9K2fzf1jJsIMLcASTnX', 'g0XId9rEs0A7zCYV4Dd2Xs5zJZN1LAGWwvxO5UT2fd9xXZY88G2iV05rdLhRsyPB', tld='us')
candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "10 Apr, 2021", "26 Apr, 2021")
walet = 1000
start = 0
end = 0
closes = []

def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")

def pourcentage_augment(start, end):
    pourcentage = 0
    if (start != 0):
        pourcentage = (float(end) - float(start)) / float(start)
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
    bought = 0

    print("received message --")

    if len(candlesticks) > RSI_PERIOD:
        np_closes = numpy.array(candlesticks)
        np_closes = convertA(np_closes)
        print(np_closes)
        rsi = talib.RSI(np_closes,RSI_PERIOD)
        print("tout les RSI jusqu'a present")
        print(rsi)
        last_rsi = rsi[-1]
        print("les rsi actuel est {}".format(last_rsi))

        for i in range(len(rsi)):
            #print("Candlestick = " + candlesticks[i][4])
            #print("les rsi actuel est {}".format(rsi[i]))
            if rsi[i] < 20:
                #print("AH")
                #print("VENDREEEEEEE {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                tmp = candlesticks[i][4]
                print("BUY I = " + str(i) + " | TMP = " + str(tmp) + "RSI  = " + str(rsi[i]))
                #print(pourcentage_augment(tmp, candlesticks[i][4]))
                walet = (walet * pourcentage_augment(start, candlesticks[i][4])) + walet
            if rsi[i] > 80 and float(candlesticks[i][4]) > float(tmp) and float(tmp) != 0:
                #print("ACHETER !!! {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                tmp = candlesticks[i][4]
                print("SELL I = " + str(i) + " | TMP = " + str(tmp) + "RSI  = " + str(rsi[i]))
                walet = (walet * pourcentage_augment(start, candlesticks[i][4])) + walet
            i += 14

on_message()
print(walet)
print(start)