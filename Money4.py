import sys
#Si 2 valeurs  identique 
re_index =[]
# converti tab de  caracteres en tab de  int 
def getInt(tab):
    acc = tab[0]
    for i in range(len(tab)):
        if i == 0:
            acc = acc * getMult(len(tab)-i)
        else:
            acc1 = tab[i] * getMult(len(tab)-i) 
            acc += acc1
    return acc
        
# Participe  à la conversion du tableau de caractère en tableau de int        
def getMult(nb):
    acc = 1
    for i in range(nb-1):
        acc = acc * 10
    return acc

# Recupère l'indice du tableau original pour le retour du résultat
def boucle(indice,val,tableau):
    #print("val:")
    #print(val)
    for i in range(len(tableau)):
            if(tableau[i] == val and i>= indice):
                #print(i)
                return i
              
# Retourne les valeurs d'achats et de ventes du tableau de prédiction        
def prediction(tableau):
    re =[]
    pos = False
    for val in tableau:
        if pos  == False  and val != max(tableau[tableau.index(val):]):
            pos  = True
            re.append(val)
        if pos == True and val > re[-1]:
            #print(re[-1])
            pos = False
            re.append(val)
    return re

# Transforme le  tableau d'entré de prédiction en tableau d'indice
def getIndex(tab,tableau):
    current_index = 0
    for val in  tab:
        
        if(len(re_index)==0):
            re_index.append(tableau.index(val))
            current_index = tableau.index(val)
        else:
            
            if(tableau.index(val) < int(current_index)):
                current_index = re_index[-1]
                test = tableau[current_index:].index(val)                
                re_index.append(boucle(current_index,val,tableau))                
            else:
                re_index.append(tableau.index(val))
                current_index =  tableau.index(val)
        current_index = re_index[-1]               
        
# Parse l'input retourne un tableau d'entier (a voir si mieux float)
def init(tab1,test):
    tmp = []
    tab = prediction(test)
    for i in range(len(tab1)):
    
        if tab1[i] != '[' and tab1[i] != ']':
            if tab1[i] != ',':
                tmp.append(int(tab1[i]))
            else:
                test.append(getInt(tmp))
                tmp = []
#  Transforme l'input  via fonction init retourne un tableau d'indexes pour une stratégie d'investissment (et pas la plus opti).                
def main(tab1):
    test = []
    tmp = []
    init(tab1,test)
    tab = prediction(test)
    getIndex(tab,test)
    return re_index
    
    
    
tab1 = sys.argv[1]
print(main(tab1))   
main(tab1)