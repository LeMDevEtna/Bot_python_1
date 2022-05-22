import json
global array_size
global total

def parse(json_data):
    parsed_json = (json.loads(json_data))
    print(json.dumps(parsed_json, indent=4, sort_keys=True))
    loaded_json = json.loads(json_data)
    for x in loaded_json:
	    print("%s: %d" % (x, loaded_json[x]))
     
def paser():
    total = 0
    with open('data.json', 'r') as f:
        distros_dict = json.load(f)
        print(len(distros_dict))
    for distro in distros_dict:
        parsing_1(distro)
        total += parsing_2(distro['floor_layout'],total)
    print(total*12)        
        
     
def parsing_1(distro):
    test = distro['height']
    print("n = ",test)     
     
def parsing_2(distro,total):
    
    #test = distro['floor_layout']
    
    for dist in distro:
        exist = "E" in  dist['orientations']
        if exist:
            #parsing_1(distro)
            rent = dist['monthly_rent']
            res = (rent*0.05)
            print("rent = ",rent*0.05)
            return  res    
          
#parsing_1() 
paser()    