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
    cursor.execute("SELECT question_id FROM app_tree WHERE parent_id ="+parent_id)
    for (x,) in cursor:
        res.append(x)
    return res

"""curseur.execute("SELECT yes_count FROM app_answer WHERE item_id = 65 and question_id = (SELECT question_id FROM app_tree WHERE depth = 0)")"""

curseur.execute("SELECT id FROM app_tree WHERE depth = 0")

for (x,) in curseur:
    print x
    
    
