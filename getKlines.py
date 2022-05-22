import config, csv
import pprint, talib, numpy
from binance.client import Client
RSI_PERIOD = 14
RSI_OVERBOUGHT = 79
RSI_OVERSOLD = 20
TRADE_SYMBOL = 'FTMUSD'
TRADE_QUANTITY = 25
in_position = False
client = Client(config.API_KEY, config.API_SECRET)
closes = []
# prices = client.get_all_tickers()

# for price in prices:
#     print(price)

csvfile = open('2021_5minutes.csv', 'w', newline='') 
candlestick_writer = csv.writer(csvfile, delimiter=',')

candlesticks = client.get_historical_klines("ADAUSDT", Client.KLINE_INTERVAL_1MINUTE, "16 Apr, 2021", "19 Apr, 2021")

for candlestick in  candlesticks:
	close  = candlestick[4]       
	closes.append(float(close))

np_closes = numpy.array(closes)
rsi = talib.RSI(np_closes,RSI_PERIOD)
print(rsi)
for idx, val in enumerate(rsi):
	if val > RSI_OVERBOUGHT and val !=0:
		if in_position:
			print("VENDREEEEEEE {}".format(TRADE_SYMBOL))
			outF = open("MomoTest1.txt",'w')
			last_price = closes[idx]
			outF.write("vendu  à :")
			outF.write(str(closes[idx]))
			outF.close()
	                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
	                    #if order_succeeded:
			in_position = False
		else:
			print("OVERBOUGHT Vous n'en possedez aucun ")            
	if val < RSI_OVERSOLD:
		if in_position:
			print("Over sold  on  {}  but you own it ".format(TRADE_SYMBOL))
		else:  
			print("ACHETER !!! {}".format(TRADE_SYMBOL))
			outF = open("MomoTest1.txt",'w')
			last_price = closes[idx]
			outF.write(" acheter  à :")
			outF.write(str(closes[idx]))
			outF.close()    
	                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
			in_position = True		

print("closes")
#print(closes)	

def my_function(tab):
	i = 0
	j = 14
	for A in tab:
		closes = tab[i:j]
		i = i+14
		j = j+14	
		if len(closes) > RSI_PERIOD:
			np_closes = numpy.array(closes)
			rsi = talib.RSI(np_closes,RSI_PERIOD)
			print("tout les RSI jusqu'a present")
			print(rsi)
			last_rsi = rsi[-1]
			print("les rsi actuel est {}".format(last_rsi))
	            
			if last_rsi > RSI_OVERBOUGHT:
				if in_position:
					print("VENDREEEEEEE {}".format(TRADE_SYMBOL))
					outF = open("MomoTest1.txt",'w')
					last_price = closes[-1]
					outF.write("vendu  à :")
					outF.write(closes[-1])
					outF.close()
	                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
	                    #if order_succeeded:
					in_position = False
				else:
						print("OVERBOUGHT Vous n'en possedez aucun ")            
				if last_rsi < RSI_OVERSOLD:
					if in_position:
						print("Over sold  on  {}  but you own it ".format(TRADE_SYMBOL))
					else:  
						print("ACHETER !!! {}".format(TRADE_SYMBOL))
						outF = open("MomoTest1.txt",'w')
						last_price = closes[-1]
						outF.write(" acheter  à :")
						outF.write(closes[-1])
						outF.close()    
	                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
						in_position = True
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2020", "12 Jul, 2020")
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017", "12 Jul, 2020")

#for candlestick in  candlesticks:
	#print(candlestick[4])
    #candlestick[0] = candlestick[0] / 1000
   # candlestick_writer.writerow(candlestick[4])

#csvfile.close()

#my_function(closes)

