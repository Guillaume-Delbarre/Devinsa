import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT yes_count FROM app_answer WHERE item_id = 7336 and question_id = 1")

for x in curseur:
    print x

curseur.execute("SELECT question_id FROM app_answer LIMIT 1")

for x in curseur:
    print x
