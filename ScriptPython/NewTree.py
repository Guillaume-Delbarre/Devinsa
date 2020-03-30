import mysql.connector

#APP_ITEM
#[Name,ID]
#APP_ANSWER
#[question_id,item_id,yes_count,no_count,yes_tfidf,no_tfidf]
#APP_TREE
#

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def extrait_item(cursor):
    res = []
    cursor.execute("SELECT name,id FROM app_item")
    for (x,y) in curseur:
        res.append([x,y])
    return res

def extrait_answer(cursor):
    res = []
    cursor.execute("SELECT question_id,item_id,yes_count,no_count,yes_tfidf,no_tfidf FROM app_answer")
    for (a,b,c,d,e,f) in cursor:
        res.append([a,b,c,d,e,f])
    return res

def extrait_tree(cursor):
    res = []
    cursor.execute("SELECT id,parent_id,choice,question_id FROM app_tree")
    for (a,b,c,d) in curseur:
        res.append([a,b,c,d])
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

def median(cursor,liste_item_id,liste_question_id):
    med = []
    summ_yes = 0
    summ_no = 0
    for question in range(len(liste_question_id)):
        for item in range(len(liste_item_id)):
            cursor.execute("SELECT yes_tfidf,no_tfidf FROM app_answer WHERE item_id = "+str(liste_item_id[item])+" and question_id = "+str(liste_question_id[question]))
            for (x,y) in cursor:
                summ_yes += x
                summ_no += y
        summ_yes = summ_yes/(len(liste_item_id))
        med.append(summ_yes)
        summ_no = summ_no/(len(liste_item_id))
        med.append(summ_no)
        summ_yes = 0
        summ_no = 0
    return med
        
a = extrait_tree(curseur)
print a[1][2]
print a[1][2]=="o"


    
    
