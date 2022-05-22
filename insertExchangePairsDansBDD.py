import websocket ,json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config
import pymongo
import bcrypt
url2= "mongodb+srv://test1:test1@gpe1.q6e09.mongodb.net/GPE-api?retryWrites=true&w=majority"
client = pymongo.MongoClient(url2)
mydb = client["GPE-api"]
u = mydb["Pair"]
db  = mydb.u


client = Client(config.API_KEY, config.API_SECRET)
v = client.get_all_tickers()
for pair in v:
    #print(pair['symbol'])
    existing_pair = u.find_one({'name' : pair['symbol']})
    if existing_pair is None:
        u.insert({'name' : pair['symbol']})
    