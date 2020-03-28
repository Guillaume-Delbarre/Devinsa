import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT yes_count FROM app_answer WHERE item_id = 7336")

for x in curseur:
    print x

print "\n."

curseur.execute("SELECT id FROM app_question WHERE title = A t il un rapport avec l'espace ?")

for x in curseur:
    print x

print "\nend"
