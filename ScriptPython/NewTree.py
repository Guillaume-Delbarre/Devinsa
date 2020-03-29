import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

curseur.execute("SELECT yes_count FROM app_answer WHERE item_id = (SELECT id FROM app_item WHERE name = 123) and question_id = (SELECT question_id FROM app_tree LIMIT 1)")

for x in curseur:
    print x

