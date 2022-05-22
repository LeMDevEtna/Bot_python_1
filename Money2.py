import json 

tableau = [11, 222, 3, 899, 24, 5, 46, 67]
tableau1 = [11, 222, 3, 899, 24, 5, 46, 67]
print(tableau)
#tableau_trie = tri_fusion(tableau)
##print(tableau_trie)

def find_element_in_list(element, list_element):
    index_element = list_element.index(element)
    if index_element != None:
        return index_element
    return -1
indice = find_element_in_list(899,tableau)
print(indice)


print(tableau[:1])
def maxi(tableau,val,prediction):
    if len(tableau)==1:
        if val < tableau[0]:
            return None
        else:
            return find_element_in_list(tableau[0], prediction)
            
    max_value = max(tableau)


    max_index = prediction.index(max_value)
    return max_index 
       
#test(tableau)
#testM = maxi(tableau[2:],222,tableau1)
position = False
res = []
for val in tableau1:
    if position == False and maxi(tableau1[find_element_in_list(val, tableau):],val,tableau) != find_element_in_list(val, tableau1):
        position = True
        res.append(find_element_in_list(val,tableau))
    if position == True and val > tableau[res[-1]]:
        res.append(find_element_in_list(val, tableau))    
print(res)   

re =[]
pos = False
for val in tableau:
    if pos  == False  and val != max(tableau[tableau.index(val):]):
        pos  = True
        re.append(val)
    if pos == True and val > re[-1]:
        print(re[-1])
        pos = False
        re.append(val)
print(re)            
#print(testM)



