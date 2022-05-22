#import libraries
import websocket ,json, pprint, talib, numpy

SOCKET =  "wss://stream.binance.com:9443/ws/ftmusdt@kline_1m"
from bs4 import BeautifulSoup
import requests
import csv
url = "https://www.binance.com/fr/support/announcement/c-48"
url2="https://www.boursedirect.fr/fr/marche/new-york-stock-exchange-inc/dow-jones-industrial-average-DJI-USD-XNYS/seance"
url3="https://www.boursedirect.fr/fr/bourse-direct/chiffres-cles"
cmc = requests.get(url3)
soup = BeautifulSoup(cmc.content, 'html.parser')
bol = False
first= True
isDiff = True
while (isDiff ==True):
    for span in  soup.find_all(class_="quotation-left"):
        first_child = next(span.children, None)
        print(first_child.string)
        for span in soup.find_all(class_="bd-streaming-select-value-last"):
            first_child1 = next(span.children, None)
        if first_child is not None and bol == False and isDiff:
            Last_one=first_child.string
            print(first_child.string)
            cmc = requests.get(url3)
         
            first =True
            soup = BeautifulSoup(cmc.content, 'html.parser')
            if first_child.string==Last_one and first==True:
                first=False
            else:
                bol =False
                print("same value")
                isDiff=False


#print(soup.find(class="css-vurnku"))
def on_open():
    print("opened connection --")

def on_close():
    print("closed connection --")
 
def on_message(ws,message):
    global closes
    print("received message --")

ws = websocket.WebSocketApp(url3,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()


