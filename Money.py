import json 
def test(prediction):
    first = 0
    res = []
    tmp = 0
    
    for val in prediction:
        if find_element_in_list(val,prediction) == 0:
            first = val
            tmp = val
            res.append(find_element_in_list(val,prediction))
        if find_element_in_list(val,prediction) > 0 and tmp !=0:
            if val > tmp:
               res.append(find_element_in_list(val,prediction))
               tmp = 0
        if find_element_in_list(val,prediction) > 0 and tmp == 0:
            if max(val,prediction[find_element_in_list(val,prediction):]) != None:
                tmp = val       
    print(res)     

def prediction(prediction):
    pred_triée = tri_fusion(prediction)
    benef = 0
    acc = 0 
    acc1 = 0 
    #for  i in range(len(prediction)):
        #acc = prediction[find_element_in_list(prediction)]
        #f i > 0:
            #acc1 =
             
    #for val in prediction:
        #if acc = val 
    #return None

def tri_fusion(tableau):
    if  len(tableau) <= 1: 
        return tableau
    pivot = len(tableau)//2
    tableau1 = tableau[:pivot]
    tableau2 = tableau[pivot:]
    gauche = tri_fusion(tableau1)
    droite = tri_fusion(tableau2)
    fusionne = fusion(gauche,droite)
    return fusionne
#Tri fusion fonction de fusion de 2 listes
def fusion(tableau1,tableau2):
    indice_tableau1 = 0
    indice_tableau2 = 0    
    taille_tableau1 = len(tableau1)
    taille_tableau2 = len(tableau2)
    tableau_fusionne = []
    while indice_tableau1<taille_tableau1 and indice_tableau2<taille_tableau2:
        if tableau1[indice_tableau1] < tableau2[indice_tableau2]:
            tableau_fusionne.append(tableau1[indice_tableau1])
            indice_tableau1 += 1
        else:
            tableau_fusionne.append(tableau2[indice_tableau2])
            indice_tableau2 += 1
    while indice_tableau1<taille_tableau1:
        tableau_fusionne.append(tableau1[indice_tableau1])
        indice_tableau1+=1
    while indice_tableau2<taille_tableau2:
        tableau_fusionne.append(tableau2[indice_tableau2])
        indice_tableau2+=1
    return tableau_fusionne
tableau = [11, 222, 3, 899, 24, 5, 46, 67]
print(tableau)
tableau_trie = tri_fusion(tableau)
print(tableau_trie)

def find_element_in_list(element, list_element):
    index_element = list_element.index(element)
    if index_element != None:
        return index_element
    return -1
indice = find_element_in_list(899,tableau)
print(indice)


print(tableau[:1])
def max(tableau,val):
    if (len(tableau = 1)):
        if(tableau[0]>val):
            return
    tmp = 0 
    for value in tableau:   
        if value > val:
            tmp = find_element_in_list(value, tableau)
            return tmp
    return None        
test(tableau)


def is_max(tableau,val):
    for i in range(len(tableau)):
        if(val < tableau[i]):
def test2(tableau):
    position =  False
    res = []
    for val in tableau:
        if max(tableau,val) == val: