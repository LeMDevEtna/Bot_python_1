#import libraries
from bs4 import BeautifulSoup
import requests
import csv
url = "https://www.boursedirect.fr/fr/bourse-direct/chiffres-cles"

cmc = requests.get(url)
soup = BeautifulSoup(cmc.content, 'html.parser')
bol = False
#results = soup(raw_resuk)
#print(soup.find('<div class="quotation-left"'))
div = soup.find_all(class_="mini-bloc streaming-row bd-streaming bd-streaming-anim-glow-rise-2-css")
print(div['data-last'])
    children = div.findChildren("bd-streaming-select-value-last")
    first_child = next(div.children, None)
    if first_child is not None and bol == False:
        print(first_child.string.strip())
        bol = True

#print(soup.find(class="css-vurnku"))





