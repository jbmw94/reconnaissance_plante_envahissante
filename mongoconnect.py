import pymongo 
import pprint
import math
import string

from pymongo.cursor import Cursor

# define the client, the database, and the collection
# the database and the collection are created at first insert 
# if needed
url_loc = "localhost"
code = 27017
data = "projet_final"
# collection = "location plante"
collection = "plante_collection"

def connection_mongo(url_loc, code, data, collection): 
    client = pymongo.MongoClient(url_loc,code)
    mydb = client[data]
    sinfun = mydb[collection]
    # sinfun2 = mydb[collection2]
    cursor = sinfun.find()
    #cursor2 = sinfun2.find()
    entries = list(cursor)
    #entries2 = list(cursor2)
    return sinfun, cursor, entries


def search_data(label, sinfun2) : 
    cd_name = (sinfun2.find_one({'Nom de référence' : label}, {'CD_NOM':1, '_id':0} ))
    verna = (sinfun2.find_one({'Nom de référence' : label}, {'Nom vernaculaire':1, '_id':0} ))
    return cd_name['CD_NOM'], verna['Nom vernaculaire']
#label = "Spiraea xbillardii Hérincq, 1857"
#sinfun, cursor, entries = connection_mongo(url_loc, code, data, collection)
#print(entries)
#cd_name, verna = search_data(label, sinfun)
#print(cd_name, verna)
def nom_ref(label) : 
    x =(label.split(" ", 2))
    
    return x[0]+' '+x[1]
    


def insert_data(label, location, sinfun) : 
    data = []        
    data.append ({"plante":label, "localisation":location})    
    sinfun.insert_many(data)

        print('done')
#sinfun, cursor, entries = connection_mongo(url_loc, code, data, collection)

#print(entries)
#nsert_data(data, location)
# sinfun, cursor, entries, sinfun2 = connection_mongo(url_loc, code, data, collection, collection2)

"""""
import jinja2
loader = jinja2.FileSystemLoader('./index.html')
env = jinja2.Environment(loader=loader)
template = env.get_template('')
print template.render(date='2012-02-8', id='123', position='here', status='Waiting')
"""""
