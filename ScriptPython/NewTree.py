import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT question_id FROM app_answer LIMIT 1")

for x in curseur:
    print x

