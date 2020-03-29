import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')


def extrait_itemID(base):
    res = []
    curseur = base.cursor()
    curseur.execute("SELECT id FROM app_item")
    for (x,) in curseur:
        res.add(x)
    return res

print extrait_itemID(base)
    
