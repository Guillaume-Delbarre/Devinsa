import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT Noms FROM app_answer")
for (table_name,) in curseur:
    print (table_name)
