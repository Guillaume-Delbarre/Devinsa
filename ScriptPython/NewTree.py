import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT no_tfidf FROM app_answer WHERE item_id = (SELECT id FROM app_item WHERE name = 123)")

for x in curseur:
    print x

