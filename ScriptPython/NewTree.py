import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def extrait_itemID(cursor):
    res = []
    cursor.execute("SELECT id FROM app_item")
    for (x,) in curseur:
        res.append(x)
    return res

def getfils(cursor,parent_id):
    res = []
    cursor.execute("SELECT id FROM app_tree WHERE parent_id ="+parent_id)
    for (x,) in cursor:
        res.append(x)
    return res

print getfils(curseur,"149235")
    
