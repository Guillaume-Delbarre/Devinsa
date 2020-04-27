import mysql.connector

#APP_ITEM
#[ID,Name]
#APP_ANSWER
#[question_id,item_id,yes_count,no_count,yes_tfidf,no_tfidf]
#APP_TREE
#[id,parent_id,choice,question_id,title]
#APP_QUESTION
#[id,title]

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

def test(cursor):
    res = []
    cursor.execute("SELECT app_answer.question_id, app_answer.item_id, yes_count, no_count, yes_tfidf, no_tfidf FROM app_answer CROSS JOIN app_question,app_item ON "+
                   "app_question.id = app_answer.question_id and app_item.id = app_anser.item_id")
    for (a,b,c,d,e,f) in cursor:
        res.append([a,b,c,d,e,f])
    return res

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
    cursor.execute("SELECT app_tree.id,parent_id,choice,question_id,title FROM app_tree,app_question WHERE app_tree.question_id = app_question.id and choice<>'p'")
    for (a,b,c,d,e) in curseur:
        res.append([a,b,c,d,e])
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
        if len(res)==2:
            return res
    return res

def creerMatrice(ligne,colonne):
    res = []
    for i in range(ligne):
        res.append([None]*colonne)
    return res

def recopierMatrice(matrice):
    res = []
    for elem in matrice:
        res.append(elem)
    return res

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            return item[0]
    return None

def compterPerso(rangQuestion,matricePerso,choix):
    res = recopierMatrice(matricePerso)
    for perso in matricePerso[1:]:
        rapport = 1
        yes_count = perso[rangQuestion][0]
        no_count = perso[rangQuestion][1]
        if choix =='o' and no_count!=0:
            rapport = yes_count/no_count
        elif choix == 'n' and yes_count!=0:
            rapport = no_count/yes_count
        elif yes_count==0 and no_count==0:
            rapport = 0
        else:
            rapport = 1
        if rapport<0.75:
            res.remove(perso)
    return res

def miseEnFormeText(text):
    return text.replace('\'',"\\'")

def avoirRangQuestion(id_question,matricePerso):
    i = 0
    for question in matricePerso[0]:
        if(id_question==question):
            return i
        i += 1
    print("Error 4")
    return

def HTMLclass(choice):
    if choice=='o':
        return 'light-green'
    if choice=='n':
        return 'light-red'
    return 'None'

def elagagePerso(question,app_tree,matricePerso,ecrire):
    if(len(matricePerso)==1):        
        ecrire += "\ntext: { name: ' Aucun personnage '}, collapsed : true\n"
        return ecrire
    elif(question[0]==1):
        ecrire += "text: { name: '"+miseEnFormeText(app_tree[0][4])+"' }, collapsed : true, children : [\n"
    else:
        listeperso = proxi(median(matricePerso),matricePerso)
        listeperso = list(set(listeperso))
        perso_median = ""
        for i in range(len(listeperso)):
            if i==0:
                perso_median += "perso1 : '"+miseEnFormeText(listeperso[i][1])+"',"
            if i==1:
                perso_median += "perso2 : '"+miseEnFormeText(listeperso[i][1])+"',"
            if i==2:
                perso_median += "perso3 : '"+miseEnFormeText(listeperso[i][1])+"',"
        perso_median = perso_median[:len(perso_median)-1]
        html = HTMLclass(question[2])
        ecrire += "\ntext: { name: '"+str(len(matricePerso)-1)+" personnage(s)',"+perso_median+", desc : '"+miseEnFormeText(question[4])+"'},HTMLclass :'"+html+"',collapsed : true, children : [\n"
    questionsFilles = getfils(question[0],app_tree)
    if(len(questionsFilles)==0):
        ecrire += "{text : {name : 'Question aléatoire'}, collapsed: true}]"
        return ecrire
    else:
        choixOui = []
        choixNon = []
        for i in range(len(questionsFilles)):
            if questionsFilles[i][2]=='o':
                choixOui = questionsFilles[i]
            elif questionsFilles[i][2] =='n':
                choixNon = questionsFilles[i]
            else:
                print("Error 3")
                return
        rangQuestion = avoirRangQuestion(question[3],matricePerso)
        matricePersoOui = compterPerso(rangQuestion,matricePerso,'o')
        matricePersoNon = compterPerso(rangQuestion, matricePerso,'n')
        ecrire += "\n{"
        if (choixOui!=[]):
            ecrire += elagagePerso(choixOui,app_tree,matricePersoOui,"")
        ecrire += "\n}, \n {"
        if (choixNon!=[]):
            ecrire += elagagePerso(choixNon,app_tree,matricePersoNon,"")
        ecrire += "\n } \n]"
        return ecrire

                
        
def median(matrice):
    med = [0]
    summ1 = 0
    summ2 = 0
    for j in range(1,len(matrice[0])):
        for i in range(1,len(matrice)):
            summ1 += matrice[i][j][2]
            summ2 += matrice[i][j][3]
        summ1 = summ1/(len(matrice)-1)
        summ2 = summ2/(len(matrice)-1)
        med.append((summ1,summ2))
        summ1,summ2 = 0,0
    return med
        
def carre(x):
    return (x)*(x)

def proxi(med,matrice):
    if len(matrice)==4:
        return [matrice[1][0],matrice[2][0],matrice[3][0]]
    elif len(matrice)==3:
        return [matrice[1][0],matrice[2][0]]
    elif len(matrice)==2:
        return [matrice[1][0]]
    dist1 = 0
    dist2 = 0
    dist3 = 0
    for j in range(1,len(matrice[0])):
        dist1 += carre(med[j][0]-float(matrice[1][j][2]))
        dist1 += carre(med[j][1]-float(matrice[1][j][3]))
        dist2 += carre(med[j][0]-float(matrice[2][j][2]))
        dist2 += carre(med[j][1]-float(matrice[2][j][3]))
        dist3 += carre(med[j][0]-float(matrice[3][j][2]))
        dist3 += carre(med[j][1]-float(matrice[3][j][3]))
    dist_aux = 0
    aux = [[matrice[1][0],dist1],[matrice[1][0],dist2],[matrice[1][0],dist3]]
    for i in range(2,len(matrice)):
        for j in range(2,len(matrice[0])):
            dist_aux += carre(med[j][0]-float(matrice[i][j][2]))
            dist_aux += carre(med[j][1]-float(matrice[i][j][3]))
        rang_maxi_dist = 0
        for k in range(len(aux)):
            if(aux[k][1]>aux[rang_maxi_dist][1]):
                 rang_maxi_dist = k
        if(dist_aux<aux[rang_maxi_dist][1]):
            aux[rang_maxi_dist][0] = matrice[i][0]
            aux[rang_maxi_dist][1] = dist_aux
        dist_aux = 0
    return [aux[0][0],aux[1][0],aux[2][0]]


def garder_questions_arbre(app_tree,app_question):
    aux = []
    for question in app_tree:
        if question[3] not in aux and type(question[3])==int:
            aux.append(question[3])
    res = []
    for ident in aux:
        for question in app_question:
            if ident==question[0]:
                res.append(question)
    return res

#Fonction qui permet de garder les reponses dune liste de questions
def garder_reponses_arbre(app_answer,liste_questions):
    res = []
    for i in range(len(liste_questions)):
        for j in range(len(app_answer)):
            if liste_questions[i][0]==app_answer[j][0]:
                res.append(app_answer[j])
    return res

def createBinarytree(app_tree):  
    resultat = []
    question_id = []
    for question in app_tree:
        if len(resultat)==0 and len(question_id)==0:
            question_id.append(question[0])
            resultat.append(question)
        if (question[1] in question_id):
            question_id.append(question[0])
            resultat.append(question)
    return resultat


def get_tfIdfCount(id_perso,app_answer,id_question):
    for answer in app_answer:
        if answer[1] == id_perso and answer[0] == id_question:
            return (answer[2],answer[3],answer[4],answer[5])
    return (0,0,0,0)

def creation_matrice_perso(app_answer,app_item,liste_questions):
    res = creerMatrice(len(app_item)+1,len(liste_questions)+1)
    for i in range(len(liste_questions)):
        res[0][i+1] = liste_questions[i][0]
    for i in range(len(app_item)):
        res[i+1][0] = (app_item[i][0],app_item[i][1])
    for i in range(1,len(res)):
        for j in range(1,len(res[0])):
            res[i][j] = get_tfIdfCount(res[i][0][0],app_answer,res[0][j])
    return res

def main(curseur):
    #On extrait chaque tables, les details sont en haut
    app_answer = extrait_app_answer(curseur)
    print(len(app_answer))
    app_item = extrait_app_item(curseur)
    print(len(app_item))
    app_tree = extrait_app_tree(curseur)
    app_question = extrait_app_question(curseur)
    print(len(app_question))
    lol = test(curseur)
    print(len(lol))
    #On elague larbre ternaire en arbre binaire
    """app_tree = createBinarytree(app_tree)
    #Dans notre liste de questions, seules celles presentes dans larbre nous interessent
    liste_questions = garder_questions_arbre(app_tree,app_question)
    #Seules les reponses aux questions de larbre nous interessent
    app_answer = garder_reponses_arbre(app_answer,liste_questions)
    #Preparation de liste_questions pour creer une matrice tfidf_oui,non pour chaque (perso,question)
    matricePerso = creation_matrice_perso(app_answer,app_item,liste_questions)
    ecrireFinal = elagagePerso(app_tree[0],app_tree,matricePerso,"")
    file = "../Web/Arbre_Binaire/script/data.js"
    ecriture = open(file,"w",encoding="utf-8")
    ecriture.write("chart_config = { chart : {container: '#tree', scrollbar: 'native', \nconnectors: { type: 'step' },\n node: { HTMLclass: 'nodeExample1' },\n "+
                        "animation: { nodeAnimation: "+'"'+"easeOutBounce"+'"'+", nodeSpeed: 700,connectorsAnimation: "+'"'+"bounce"+'"'+", connectorsSpeed: 700 }},\n"+
                        "nodeStructure : {")
    
    ecriture.write(ecrireFinal)
    ecriture.write(" } \n };")
    ecriture.close
    print("end\n")"""
    
main(curseur)
