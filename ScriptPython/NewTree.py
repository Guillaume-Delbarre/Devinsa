import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT 'Oui A t il un rapport avec l'espace ?' 1 FROM app_item WHERE Noms = Onyx")
for (table_name,) in curseur:
    print (table_name)
