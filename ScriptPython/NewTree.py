import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def extrait_itemID(curseur):
    res = []
    curseur.execute("SELECT id FROM app_item")
    for (x,) in curseur:
        res.append(x)
    return res

    
    
