import mysql.connector

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def extrait_itemID(cursor):
    res = []
    cursor.execute("SELECT id FROM app_item")
    for (x,) in curseur:
        res.append(x)
    return res

def extrait_questionID(cursor):
    res = []
    cursor.execute("SELECT question_id FROM app_answer")
    for (x,) in cursor:
        res.append(x)
    return res

def getfils(cursor,parent_id):
    res = []
    cursor.execute("SELECT id FROM app_tree WHERE parent_id ="+str(parent_id)+" and choice = 'o' ")
    for (x,) in cursor:
        res.append(x)
    cursor.execute("SELECT id FROM app_tree WHERE parent_id ="+str(parent_id)+" and choice = 'n' ")
    for (x,) in cursor:
        res.append(x)
    return res



def compterPerso(cursor,liste_item_id,app_tree_id,choice):
    res = recopierTableau(liste_item_id)
    yes_count = 0
    no_count = 0
    rapport = 1
    for i in range(len(liste_item_id)):
        cursor.execute("SELECT yes_count FROM app_answer WHERE item_id = "+str(liste_item_id[i])+" and question_id = (SELECT question_id FROM app_tree WHERE id = "+str(app_tree_id)+")")
        for (x,) in cursor:
            yes_count = x
        cursor.execute("SELECT no_count FROM app_answer WHERE item_id ="+str(liste_item_id[i])+" and question_id = (SELECT question_id FROM app_tree WHERE id ="+str(app_tree_id)+")")
        for (x,) in cursor:
            no_count = x
        if choice == "o" and no_count !=0:
            rapport = yes_count/no_count
        elif choice == "n" and yes_count!=0:
            rapport = no_count/yes_count
        else:
            rapport = 1
        if rapport<0.75:
            res.remove(liste_item_id[i])
    return res
                
        
def recopierTableau(tableau):
    res = []
    for i in range(len(tableau)):
        res.append(tableau[i])
    return res

def median(liste_item_id,liste_question_id):
    med = []
    summ = 0
    

print extrait_questionID(curseur)

    
    
