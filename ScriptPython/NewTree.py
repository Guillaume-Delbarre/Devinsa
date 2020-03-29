import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT id FROM app_answer WHERE question_id ="+str(x)+" LIMIT 1")

for (x,) in curseur:
    print x
    print type(x)

