import mysql.connector
import multiprocessing as mp

#APP_ITEM
#[ID,Name]
#APP_ANSWER
#[question_id,item_id,yes_count,no_count,yes_tfidf,no_tfidf]
#APP_TREE
#[id,parent_id,choice,question_id]
#APP_QUESTION
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
    cursor.execute("SELECT id,parent_id,choice,question_id FROM app_tree WHERE depth<8")
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
            res.append(app_tree[i])
        if len(res)==3:
            return res
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

def median(app_item,app_answer,app_question,med,compteur):
    if compteur==len(app_question):
        return med
    else:
        next_app_answer = recopierMatrice(app_answer)
        summ_yes = 0
        summ_no = 0
        for k in range(len(app_answer)):
            for item in range(len(app_item)):
                if app_answer[k][1]==app_item[item][0] and app_answer[k][0]==app_question[compteur][0]:
                    summ_yes += app_answer[k][4] 
                    summ_no += app_answer[k][5]
                    next_app_answer.remove(app_answer[k])
        summ_yes = summ_yes/(len(app_item))
        summ_no = summ_no/(len(app_item))
        med.append([summ_yes,summ_no,app_answer[0]])
        compteur += 1
        return median(app_item,next_app_answer,app_question,med,compteur)
        
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

def garder_questions_arbre(app_tree,app_question):
    aux = []
    for i in range(len(app_tree)):
        if app_tree[i][3] not in aux and type(app_tree[i][3])==int:
            aux.append(app_tree[i][3])
    res = []
    for i in range(len(aux)):
        for j in range(len(app_question)):
            if aux[i]==app_question[j][0]:
                res.append(app_question[j])
    return res
                
def garder_reponses_arbre(app_answer,liste_questions):
    res = []
    for i in range(len(liste_questions)):
        for j in range(len(app_answer)):
            if liste_questions[i][0]==app_answer[j][0]:
                res.append(app_answer[j])
    return res

def elaguer_app_tree(app_tree,question,res):
    res.append(question)
    fils = getfils(question[0],app_tree)
    if len(fils)==0:
        return
    elif len(fils) == 3:
        aux = recopierMatrice(app_tree)
        for i in range(len(fils)):
            if fils[i][2] == 'p':
                fils.remove(fils[i])
        elaguer_app_tree(aux,fils[0],res)
        elaguer_app_tree(aux,fils[1],res)
        return res
    else:
        print("Error\n")
        return res

def creation_matrice_perso(app_answer,app_item,liste_questions):
    res = [[None]*(2*len(liste_questions))]*(len(app_item)+1)
    liste_questions = modifier_liste_questions(liste_questions)
    print(liste_questions)
    for i in range(1,len(liste_questions)):
        res[0][i] = liste_questions[i]
        print res[0][i][0]
    for i in range(len(app_item)):
        res[i+1][0] = app_item[i][1]
        for j in range(1,len(res[0]),2):
            id_question = res[0][j]
            for k in range(len(app_answer)):
                if app_answer[k][1] == app_item[i][0] and app_answer[k][0] == id_question:
                    res[i][j] = app_answer[k][4]
                    res[i][j+1] = app_answer[k][5]
    print [res[1][0],res[1][1],res[1][2]]
    print [res[2][0],res[2][1],res[2][2]]
    print [res[3][0],res[3][1],res[3][2]]
    return res
    

            

def modifier_liste_questions(liste_questions):
    res = [None]*(2*(len(liste_questions)))
    for i in range(1,len(liste_questions)):
        res[(2*i)-1] = liste_questions[i]
        res[(2*i)] = liste_questions[i]
    return res

def init(curseur):
    app_answer = extrait_app_answer(curseur)
    app_item = extrait_app_item(curseur)
    app_tree = extrait_app_tree(curseur)
    app_question = extrait_app_question(curseur)
    app_tree = elaguer_app_tree(app_tree,app_tree[0],[])
    liste_questions = garder_questions_arbre(app_tree,app_question)
    app_answer = garder_reponses_arbre(app_answer,liste_questions)
    creation_matrice_perso(app_answer,app_item,liste_questions)
    

    
init(curseur)



