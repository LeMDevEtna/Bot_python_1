import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config,csv
import os

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_5m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 77
RSI_OVERSOLD = 23.3
TRADE_SYMBOL = 'FTMUSD'
TRADE_QUANTITY1 = 0
TRADE_QUANTITY2 = 0
closes = []
last_price = 0
in_position  = False

#csvfile = open('RSITESTFinal.txt', 'w', newline='') 
#candlestick_writer = csv.writer(csvfile, delimiter=',')
                     


client = Client(config.API_KEY, config.API_SECRET, tld='us')
print(" je suis passer la ")
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order ...")
        order = client.create_order(symbol=symbol,side = side,type = order_type,quantity = quantity)
        #print(order)
    except Exception as e:
        return False
    return True    
    
def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")
 
def get_Max_Usdt():
    balance = client.get_asset_balance(asset='USDT')
    print(balance['free'])
    return float(balance['free'])

def get_Max_FTM():
    balance = client.get_asset_balance(asset='FTM')
    print(balance['free'])
    return float(balance['free'])      
    #fonction get max usdt quantity


def on_message(ws,message):
    global tmp2
    global closes
    global walet
    global tmp2
    global commission 
    global commission2
    global ttc
    tmp2=0
    global MaxUsdt
    bought = 0
    MaxUsdt = get_Max_Usdt()
    MaxFTM = get_Max_FTM()
    TRADE_QUANTITY1 = MaxUsdt
    TRADE_QUANTITY2 = MaxFTM
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
        #print(closes)

        if len(closes) > RSI_PERIOD:

            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            #print("tout les RSI jusqu'a present")
            #print(rsi)
            outF = open("Resultat_Bot_Fil_Rouge.txt",'a')
            outF.write(" rsi  à : {} " . str(rsi[-1]))
            outF.close() 
            last_rsi = rsi[-1]
            print("les rsi actuel est {}".format(last_rsi))
            
            if last_rsi > RSI_OVERBOUGHT and last_price < json_message['k']['l']:
                if in_position:
                    TRADE_QUANTITY2 = get_Max_FTM()
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY2, TRADE_SYMBOL)

                if order_succeeded:

                    in_position = False
                    print("VENDRE {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                    outF = open("Resultat_Bot_Fil_Rouge.txt",'a')
                    outF.write(" vendu  à : {} " . str(json_message['k']['l']))
                    outF.write(" bill   : {} " . str(order_succeeded))
                    commission2  = commission2 + ((float(json_message['k']['l']) * 0.1) /100)
                    outF.write("  commissionVentePredi  : {} " . str(commission2))
                    outF.close() 

                else:

                    print("OVERBOUGHT Vous n'en possedez aucun ")            
            if last_rsi < RSI_OVERSOLD and get_Max_Usdt > 0 :

                if in_position:
                    print("Over sold  on  {}  deja en  possession  ".format(TRADE_SYMBOL))
                else:  
                    TRADE_QUANTITY1 = get_Max_Usdt()
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY1, TRADE_SYMBOL)
                if order_succeeded:

                    in_position = True
                    print("ACHETER  {} rsi :{}".format(TRADE_SYMBOL).format(last_rsi))
                    commission = commission + ((float(json_message['k']['l']) * 0.1) /100)
                    outF = open("Resultat_Bot_Fil_Rouge.txt",'a')
                    last_price = json_message['k']['l']
                    outF.write(" acheter  à : {} " . str(json_message['k']['l']))
                    outF.write(" bill   : {} " . str(order_succeeded))
                    outF.write("  commissionAchatPredi  : {} " . str(commission2))
                    outF.close()


ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()
                      