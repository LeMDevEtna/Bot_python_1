import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv
#import configmoha
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
#csvfile = open('RSITESTFinal.txt', 'w', newline='')
#candlestick_writer = csv.writer(csvfile, delimiter=',')


#client = Client(configmoha.API_KEY, configmoha.API_SECRET)
client = Client('ZO4DljUT8x1BuqtNGk29oW1EayLQo3ai2Z8pT9Af4DtsZ9K2fzf1jJsIMLcASTnX', 'g0XId9rEs0A7zCYV4Dd2Xs5zJZN1LAGWwvxO5UT2fd9xXZY88G2iV05rdLhRsyPB', tld='us')

candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1WEEK, "16 Apr, 2021", "19 Apr, 2021")

print(candlesticks)
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

            #if last_rsi > RSI_OVERBOUGHT and last_price < json_message['k']['l']:
                #if in_position:
                #print("VENDREEEEEEE {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                #outF = open("MomoTest1.txt",'w')
                #outF.write(" vendu  à :")
                #outF.write(json_message['k']['l'])
                #outF.close()
                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                    #    in_position = False
                #else:
                    #print("OVERBOUGHT Vous n'en possedez aucun ")
            #if last_rsi < RSI_OVERSOLD:
                #if in_position:
                    #print("Over sold  on  {}  but you own it ".format(TRADE_SYMBOL))
                #else:
                #print("ACHETER !!! {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                #outF = open("MomoTest1.txt",'w')
                #last_price = json_message['k']['l']
                #outF.write(" acheter  à :")
                #outF.write(json_message['k']['l'])
                #outF.close()
                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                         #in_position = True

#ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
#ws.run_forever()
#outF.close()