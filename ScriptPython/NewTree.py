import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT item_id FROM app_answer LIMIT 5")

for x in curseur:
    print x

print "\n."

curseur.execute("SELECT id FROM app_item WHERE name = 123")

for x in curseur:
    print x

print "\nend"
