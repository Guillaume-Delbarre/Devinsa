import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT question_id FROM app_answer LIMIT 5")
for (table_name,) in curseur:
    print (table_name)
