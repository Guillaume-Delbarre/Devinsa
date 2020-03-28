import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT * FROM app_item LIMIT 5")
for (table_name,) in curseur:
    for x in (table_name):
        print x
