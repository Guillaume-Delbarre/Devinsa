import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursos()

curseur.execute("SHOW DATABASES")
for x in mycursos:
    print x
