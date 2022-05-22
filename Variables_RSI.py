price = float(0)
in_position = True
##
SOCKET =  "wss://stream.binance.com:9443/ws/reefusdt@kline_1m"
RSI_PERIOD = 14
in_position = True
RSI_OVERBOUGHT = 78.3
RSI_OVERSOLD = 23.9
TRADE_SYMBOL = 'REEFUSDT'
TRADE_SYMBOL_1 = 'REEF'
TRADE_SYMBOL_2 = 'USDT'

closes = []
##


client
TRADE_QUANTITY1
TRADE_QUANTITY2
precision
step_size_reef              
step_size_usdt             
ticks = {}

client = Client(config.API_KEY, config.API_SECRET)
client2 = Client(configV.API_KEY, configV.API_SECRET)
for filt in client.get_symbol_info(TRADE_SYMBOL)['filters']:
                if filt['filterType'] == 'LOT_SIZE':
                    step_size_reef= ticks[TRADE_SYMBOL_1] = filt['stepSize']
                    step_size_usdt=ticks[TRADE_SYMBOL_2] = filt['stepSize']
#print(step_size_reef)
#print(step_size_usdt)
step_size_reef = float(step_size_reef)
step_size_usdt = float(step_size_usdt)

def get_usdt():
    try:
        balance = client.get_asset_balance(asset=TRADE_SYMBOL_2)
        print("M Balance Token wanted {}" . str(TRADE_SYMBOL_1))
        print("M Balance Usdt {}" . format(balance))
    except Exception as e:
        return 0
    return balance['free']

def get_reef():
    try:
        balance = client.get_asset_balance(asset=TRADE_SYMBOL_1)
        print("M Balance stable coin {}" . str(TRADE_SYMBOL_1))
        print("M Balance  {}" . format(balance))
    except Exception as e:
        return 0
    return balance['free']