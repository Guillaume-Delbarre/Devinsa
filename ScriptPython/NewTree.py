import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

a = curseur.execute("SELECT yes_count FROM app_answer WHERE question_id = 235 AND id = 12 LIMIT 5")

print a
