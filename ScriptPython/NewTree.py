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
    cursor.execute("SELECT app_tree.id,parent_id,choice,question_id,title FROM app_tree,app_question WHERE app_tree.question_id = app_question.id and app_tree.choice<>'p' and depth<4")
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

def compterPerso(rangQuestion,matricePerso,choix):
    res = recopierMatrice(matricePerso)
    for i in range(1,len(matricePerso)):
        rapport = 1
        yes_count = matricePerso[i][rangQuestion][0]
        no_count = matricePerso[i][rangQuestion][1]
        if choix =='o' and no_count!=0:
            rapport = yes_count/no_count
        elif choix == 'n' and yes_count!=0:
            rapport = no_count/yes_count
        elif yes_count==0 and no_count==0:
            rapport = 0
        else:
            rapport = 1
        if rapport<0.75:
            res.remove(matricePerso[i])
    return res

def miseEnFormeText(text):
    return text.replace('\'',"\\'")

def avoirRangQuestion(id_question,matricePerso):
    for i in range(len(matricePerso[0])):
        if(id_question==matricePerso[0][i]):
            return i
    print("Error 4")
    return

def HTMLclass(choice):
    if choice=='o':
        return 'light-green'
    if choice=='n':
        return 'light-red'
    return 'None'

def elagagePerso(question,app_tree,matricePerso,ecriture):
    if(len(matricePerso)==1):        
        ecriture.write("questionid_"+str(question[0])+" = {parent: questionid_"+str(question[1])+", text: { name: ' Personnages restants : 0'}, collapsed : true};\n")
    else:
        if(question[0]==1):
            ecriture.write("questionid_1 = {text: { name: '"+miseEnFormeText(app_tree[0][4])+"' }, collapsed : true};\n")
        else:
            rangPersoMedian = proxi(median(matricePerso),matricePerso)
            for i in range(len(rangPersoMedian)):
                perso_median += rangPersoMedian[i]+","
            perso_median = perso_median[:len(perso_median)-1]
            html = HTMLclass(question[2])
            ecriture.write("questionid_"+str(question[0])+" = {parent: questionid_"+str(question[1])+", HTMLclass :'"+html+"', text: { name: ' Personnages restants : "+str(len(matricePerso)-1)+" Personnage median :"+miseEnFormeText(perso_median)+"', desc : 'Prochaine question : "+miseEnFormeText(question[4])+"'}, collapsed : true};\n")
    questionsFilles = getfils(question[0],app_tree)
    if(len(questionsFilles)==0):
        return
    elif (len(questionsFilles)==2):
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
        elagagePerso(choixOui,app_tree,matricePersoOui,ecriture)
        elagagePerso(choixNon,app_tree,matricePersoNon,ecriture)
        return
    else:
        print("Error 2 ")
        return
                
        
def recopierMatrice(matrice):
    res = []
    for i in range(len(matrice)):
        res.append(matrice[i])
    return res

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
    dic = {}
    if len(matrice)==4:
        return [1,2,3]
    elif len(matrice)==3:
        return [1,2]
    elif len(matrice)==2:
        return [1]
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
    dic = {matrice[1][0] : dist1, matrice[2][0] : dist2, matrice[3][0] : dist3}
    for i in range(2,len(matrice)):
        for j in range(2,len(matrice[0])):
            dist_aux += carre(med[j][0]-float(matrice[i][j][2]))
            dist_aux += carre(med[j][1]-float(matrice[i][j][3]))
        if(dist_aux<max(dic.values())):
           dic.pop(dic.index(max(dic.values())))
           dic[matrice[i][0]] = dist_aux
        dist_aux = 0
    return dic.keys()


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

#Fonction qui permet de garder les reponses dune liste de questions
def garder_reponses_arbre(app_answer,liste_questions):
    res = []
    for i in range(len(liste_questions)):
        for j in range(len(app_answer)):
            if liste_questions[i][0]==app_answer[j][0]:
                res.append(app_answer[j])
    return res

#Fonction qui permet de passer de larbre ternaire a larbre binaire
def elaguer_app_tree(app_tree,question,res):
    res.append(question)
    fils = getfils(question[0],app_tree)
    if len(fils)==0:
        return
    elif len(fils) == 2:
        aux = recopierMatrice(app_tree)
        elaguer_app_tree(aux,fils[0],res)
        elaguer_app_tree(aux,fils[1],res)
        return res
    else:
        print("Error 1 \n")
        return res

#Fonction qui permet de creer la matrice question par colonne perso par ligne et tfd_idf en valeur
def creation_matrice_perso(app_answer,app_item,liste_questions):
    res = creerMatrice(len(app_item)+1,len(liste_questions)+1)
    for i in range(len(liste_questions)):
        res[0][i+1] = liste_questions[i][0]
    for i in range(len(app_item)):
        res[i+1][0] = app_item[i][1]
        for j in range(1,len(res[0])):
            for k in range(len(app_answer)):
                if app_answer[k][1] == app_item[i][0] and app_answer[k][0] == res[0][j]:
                    #               (yes_count,no_count,yes_tfidf,no_tfidf)
                    res[i+1][j] = (app_answer[k][2],app_answer[k][3],app_answer[k][4],app_answer[k][5])
    return res
    

            
#Fonction qui permet de doubler les questions pour correspondre tfidf_oui et tfidf_non

def remplir_matricePerso(matricePerso):
    res = recopierMatrice(matricePerso)
    for i in range(len(matricePerso)):
        for j in range(len(matricePerso[0])):
            if matricePerso[i][j]==None:
                matricePerso[i][j] = (0,0,0,0)
    return res

def creer_chart_config(app_tree):
    res = ""
    for i in range(len(app_tree)):
        res += "questionid_"+str(app_tree[i][0])+",\n"
    return res

def main(curseur):
    #On extrait chaque tables, les details sont en haut
    app_answer = extrait_app_answer(curseur)
    app_item = extrait_app_item(curseur)
    app_tree = extrait_app_tree(curseur)
    app_question = extrait_app_question(curseur)
    #On elague larbre ternaire en arbre binaire
    app_tree = elaguer_app_tree(app_tree,app_tree[0],[])
    #Dans notre liste de questions, seules celles presentes dans larbre nous interessent
    liste_questions = garder_questions_arbre(app_tree,app_question)
    #Seules les reponses aux questions de larbre nous interessent
    app_answer = garder_reponses_arbre(app_answer,liste_questions)
    #Preparation de liste_questions pour creer une matrice tfidf_oui,non pour chaque (perso,question)
    matricePerso = creation_matrice_perso(app_answer,app_item,liste_questions)
    matricePerso = remplir_matricePerso(matricePerso)
    file = "../Web/Arbre_Binaire/Treejavascript.js"
    ecriture = open(file,"w",encoding="utf-8")
    chart_config_init = "chart_config = [\n{container: '#basic-example',\nconnectors: { type: 'straight' },\n node: { HTMLclass: 'nodeExample1' },\n animation: { nodeAnimation: "+'"'+"easeOutBounce"+'"'+", nodeSpeed: 700,connectorsAnimation: "+'"'+"bounce"+'"'+", connectorsSpeed: 700 }},\n"
    elagagePerso(app_tree[0],app_tree,matricePerso,ecriture)
    chart_config = creer_chart_config(app_tree)
    chart_config = chart_config_init + chart_config
    chart_config = chart_config[0:len(chart_config)-2]
    chart_config += "];"
    ecriture.write(chart_config)
    ecriture.close
    print("end\n")
    
main(curseur)



