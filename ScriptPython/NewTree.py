import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT yes_tfidf FROM app_answer WHERE item_id = 7336 and question_id = 235")

for x in curseur:
    print x

curseur.execute("SELECT title FROM app_answer WHERE id = 235")

for x in curseur:
    print x
