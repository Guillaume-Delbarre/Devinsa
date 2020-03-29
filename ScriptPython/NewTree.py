import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def extrait_itemID(cursor):
    res = []
    cursor.execute("SELECT id FROM app_item")
    for (x,) in curseur:
        res.append(x)
    return res

def getfils(cursor,parent_id):
    res = []
    cursor.execute("SELECT question_id FROM app_tree WHERE parent_id ="+parent_id)
    for (x,) in cursor:
        res.append(x)
    return res



def compterPerso(cursor,liste_item_id,app_tree_id,choice):
    res = recopierTableau(liste_item_id)
    yes_count = 0
    no_count = 0
    rapport = 1
    for i in range(len(liste_item_id)):
        cursor.execute("SELECT yes_count FROM app_answer WHERE item_id ="+str(liste_item_id[i])+" and question_id = (SELECT question_id FROM app_tree WHERE id ="+str(app_tree_id)+"")
        for (x,) in cursor:
            yes_count = x
        cursor.execute("SELECT no_count FROM app_answer WHERE item_id ="+str(liste_item_id[i])+" and question_id = (SELECT question_id FROM app_tree WHERE id ="+str(app_tree_id)+"")
        for (x,) in cursor:
            no_count = x
        if choice == "o":
            rapport = yes_count/no_count
        if choice == "n":
            rapport = no_count/yes_count
        if rapport<0.75:
            res.remove(liste_item_id[i])
    return res
                
        

def recopierTableau(tableau):
    res = []
    for i in range(len(tableau)):
        res.append(tableau[i])
    return i

print compterPerso(curseur,extrait_itemID(curseur),1,"o")


    
    
