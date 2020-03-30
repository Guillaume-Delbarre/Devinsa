import mysql.connector

#APP_ITEM
#[ID,Name]
#APP_ANSWER
#[question_id,item_id,yes_count,no_count,yes_tfidf,no_tfidf]
#APP_TREE
#[id,parent_id,choice,question_id]
#app_question
#[id,title]

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def extrait_app_item(cursor):
    res = []
    cursor.execute("SELECT id,name FROM app_item")
    for (x,y) in curseur:
        res.append([x,y])
    return res

def extrait_app_answer(cursor):
    res = []
    cursor.execute("SELECT question_id,item_id,yes_count,no_count,yes_tfidf,no_tfidf FROM app_answer")
    for (a,b,c,d,e,f) in cursor:
        res.append([a,b,c,d,e,f])
    return res

def extrait_app_tree(cursor):
    res = []
    cursor.execute("SELECT id,parent_id,choice,question_id FROM app_tree")
    for (a,b,c,d) in curseur:
        res.append([a,b,c,d])
    return res

def extrait_app_question(cursor):
    res = []
    cursor.execute("SELECT id,title FROM app_question")
    for (a,b) in cursor:
        res.append([a,b])
    return res

def getfils(parent_id,app_tree):
    res = []
    for i in range(len(app_tree)):
        if app_tree[i][1]==parent_id:
            res.append(app_tree[i][0])
    return res



def compterPerso(app_item,app_answer,question_id,choice):
    res = recopierMatrice(app_item)
    yes_count = 0
    no_count = 0
    rapport = 1
    for i in range(len(app_item)):
        for j in range(len(app_answer)):
            if app_item[i][0]==app_answer[j][1] and app_answer[j][0]==question_id:
                yes_count = app_answer[j][2]
                no_count = app_answer[j][3]
        if choice == "o" and no_count !=0:
            rapport = yes_count/no_count
        elif choice == "n" and yes_count!=0:
            rapport = no_count/yes_count
        else:
            rapport = 1
        if rapport<0.75:
            res.remove(app_item[i])
    return res
                
        
def recopierMatrice(matrice):
    res = []
    for i in range(len(matrice)):
        res.append(matrice[i])
    return res

def median(app_item,app_answer):
    med = []
    summ_yes = 0
    summ_no = 0
    for question in range(len(app_answer)):
        for item in range(len(app_item)):
            if app_answer[question][1]==app_item[item][0]:
                summ_yes += app_answer[question][4] 
                summ_no += app_answer[question][5]
        summ_yes = summ_yes/(len(app_item))
        summ_no = summ_no/(len(app_item))
        med.append([summ_yes,summ_no,app_answer[0]])
        summ_yes = 0
        summ_no = 0
    return med
        
def carre(x):
    return (x)*(x)


def proxi(med,app_item,app_answer):
    dist_aux = 0
    for i in range(len(app_answer)):
        for j in range(len(med)):
            if app_item[0][0] == app_answer[i][1] and app_answer[i][0] == med[j][2]:
                dist_aux += carre(app_answer[i][2]-med[j][0])
                dist_aux += carre(app_answer[i][3]-med[j][1])
    res = app_item[0]
    dist = dist_aux
    dist_aux = 0
    for k in range(len(app_item)):
        for j in range(len(med)):
            for i in range(len(app_answer)):
                if app_item[k][0] == app_answer[i][1] and app_answer[i][0] == med[j][2]:
                    dist_aux += carre(app_answer[i][2]-med[j][0])
                    dist_aux += carre(app_answer[i][3]-med[j][1])
        if(dist_aux<dist):
            dist = dist_aux
            res = app_item[k]
        dist_aux = 0
    return res
                
app_question = extrait_app_question(curseur)

print len(app_question)
    
    
