import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 55
RSI_OVERSOLD = 45
TRADE_SYMBOL = 'FTMUSD'
TRADE_QUANTITY = 25
closes = []
in_position  = False
#client = Client(config.API_KEY, config.API_SECRET, tld='us')
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
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
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            print("tout les RSI jusqu'a present")
            print(rsi)
            last_rsi = rsi[-1]
            print("les rsi actuel est {}".format(last_rsi))
            
            if last_rsi > RSI_OVERBOUGHT:
                #if in_position:
                print("VENDREEEEEEE {}".format(TRADE_SYMBOL))
                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                    #    in_position = False
                #else:
                    #print("OVERBOUGHT Vous n'en possedez aucun ")            
            if last_rsi < RSI_OVERSOLD:
                #if in_position:
                    #print("Over sold  on  {}  but you own it ".format(TRADE_SYMBOL))
                #else:  
                print("ACHETER !!! {}".format(TRADE_SYMBOL))    
                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                        #in_position = True
                        
ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()
