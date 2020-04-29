import mysql.connector
import numpy as np

#APP_TREE
#[id,parent_id,choice,question_id,title]
#VECTEUR
#[id_item,name,id_question,title,yes_tfidf,no_tfidf,yes_count,no_count]



#Requête SQL permettant d'extraire TFIDF et COUNT pour chaque personnage à chaque question répondu
#Si le personnage n'a pas de données à la question répond None
#Les questions et personnages sont ordonnés
def vector(cursor):
    res = []
    cursor.execute("SELECT idg,name,id,title,yes_tfidf,no_tfidf,yes_count,no_count FROM ( "+
                   "SELECT name,title,id,idg FROM ( "+
                   "SELECT id AS idg, name FROM app_item where id in "+
                   "(Select distinct item_id from app_answer)) AS itemCROSS JOIN "+
                   "(select distinct id,title from app_question where id IN"+
                   "(select distinct question_id from app_answer)) as t0 ) AS t1 LEFT JOIN"+
                   "(select item_id,question_id,yes_tfidf,no_tfidf,yes_count,no_count from app_answer) as a ON"+
                   " t1.id=a.question_id AND t1.idg=a.item_id ORDER BY name,title")
    for (a,b,c,d,e,f,g,h) in cursor:
        res.append([a,b,c,d,e,f,g,h])
    return res

#Requête SQL pour extraire les données de l'arbre
#On retire les choix "Je ne sais pas" car pas important
def extrait_app_tree(cursor):
    res = []
    cursor.execute("SELECT app_tree.id,parent_id,choice,question_id,title FROM app_tree,app_question WHERE app_tree.question_id = app_question.id and choice<>'p' and depth<3")
    for (a,b,c,d,e) in curseur:
        res.append([a,b,c,d,e])
    return res

def getfils(parent_id,app_tree):
    res = []
    for question in app_tree:
        if question[1]==parent_id:
            res.append(question)
        if len(res)==2:
            return res
    return res

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            return item[0]
    return None

#CompterPerso permet d'enlever les personnages qui ne correspondent pas à la réponse de la question
#on rajoute +1 au count car on ne peut pas diviser par 0
#Toutes les réponses Oui sont en rang pair, les réponses Non en rang impair +1
#Par conséquent si le rang est pair le Non correspondant se situe à +1
#Si le rang est impair le rang Oui correspondant se situe à -1
def compterPerso(rangQuestion,count,tfidf,itemByOrder):
    if rangQuestion%2==0:
        divise = 1
    else:
        divise = -1
    liste_rapport = (count[:,rangQuestion]+1)/(count[:,(rangQuestion+divise)]+1)
    index_remove = []
    for i in range(liste_rapport.shape[0]):
        if liste_rapport[i]<=1:
            index_remove.append(i)
    return np.delete(count,index_remove,0),np.delete(tfidf,index_remove,0),np.delete(itemByOrder,index_remove,0)
            
            
#Fonction simple permettant d'éviter les erreurs à l'écriture dans le JS/JSON
def miseEnFormeText(text):
    return text.replace('\'',"\\'")

#Permet de donner le rang de la question dans les matrice COUNT/TFIDF
def avoirRangQuestion(id_question,questionOrder):
    i = 0
    for question in questionOrder:
        if(id_question==question[0]):
            return i
        #On incrémente de 2 car les matrices contiennent une colonne Oui et une colonne Non
        #Chaque question suivante se trouve donc 2 Colonnes plus loin
        i += 2
    print("Error avoirRangQuestion")
    return

#Fonction simple permettant de donner la couleur aux noeuds en fonction du choix fait
def HTMLclass(choice):
    if choice=='o':
        return 'light-green'
    if choice=='n':
        return 'light-red'
    return 'None'

#Fonction principal qui créé le JS/JSON
def elagagePerso(question,app_tree,tfidf,count,questionOrder,itemOrder,ecrire):
    #S'il ne reste aucun personnage
    if(itemOrder.shape[0]==0):        
        ecrire += "\ntext: { name: ' Aucun personnage '}, collapsed : true\n"
        return ecrire
    #Si c'est la première question : cas spécifique
    elif(question[0]==1):
        ecrire += "text: { name: '"+miseEnFormeText(app_tree[0][4])+"' }, collapsed : true, children : [\n"
    else:
        #On identifie les personnages les plus proches du perso médian
        listeperso = proxi(median(matricePerso),matricePerso)
        listeperso = list(set(listeperso))
        perso_median = ""
        #On met en forme pour le JS/JSON
        for i in range(len(listeperso)):
            if i==0:
                perso_median += "perso1 : '"+miseEnFormeText(listeperso[i][1])+"',"
            if i==1:
                perso_median += "perso2 : '"+miseEnFormeText(listeperso[i][1])+"',"
            if i==2:
                perso_median += "perso3 : '"+miseEnFormeText(listeperso[i][1])+"',"
        perso_median = perso_median[:len(perso_median)-1]
        html = HTMLclass(question[2])
        #On rajoute les données
        ecrire += "\ntext: { name: '"+str(len(itemOrder))+" personnage(s)',"+perso_median+", desc : '"+miseEnFormeText(question[4])+"'},HTMLclass :'"+html+"',collapsed : true, children : [\n"
    #On cherche les children de la question
    questionsFilles = getfils(question[0],app_tree)
    #Si aucun enfant
    if(len(questionsFilles)==0):
        ecrire += "{text : {name : 'Fin'}, collapsed: true}]"
        return ecrire
    else:
        #Chaque enfant correspond à une réponse Oui/Non de la question
        choixOui = []
        choixNon = []
        for question in questionsFilles:
            if question[2]=='o':
                choixOui = question
            elif question[2] =='n':
                choixNon = question
            else:
                print("Error 3")
                return
        #On compte les personnages pour la réponse Oui et la réponse Non
        rangQuestion = avoirRangQuestion(question[3],questionOrder)
        count_yes,tfidf_yes,itemOrder_yes = compterPerso(rangQuestion,count,tfidf,itemOrder)
        count_no,tfidf_no,itemOrder_no = compterPerso(rangQuestion+1,count,tfidf,itemOrder)
        ecrire += "\n{"
        #Puis on relance notre fonction avec les questions enfants
        if (choixOui!=[]):
            ecrire += elagagePerso(choixOui,app_tree,tfidf_yes,count_yes,questionOrder,itemOrder_yes,"")
        ecrire += "\n}, \n {"
        if (choixNon!=[]):
            ecrire += elagagePerso(choixNon,app_tree,tfidf_no,count_no,questionOrder,itemOrder_no,"")
        ecrire += "\n } \n]"
        return ecrire

def proxi(tfidf):
    moyen = np.mean(tfidf,0)
    dist = (tfidf-moyen)**2
    dist = np.sum(dist,1)
    print(dist)

#Fonction permettant de créer l'arbre binaire
#Elle enlève tous les sous-arbres correspondant au choix "Je ne sais pas"
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

#Fonction renvoyant la liste des questions dans l'ordre
def questionByOrder(vecteur):
    res = []
    for info in vecteur:
        if (info[2],info[3]) not in res:
            res.append((info[2],info[3]))
        else:
            return res

#Fonction renvoyant la liste des personnages dans l'ordre
def itemByOrder(vecteur):
    res = []
    for info in vecteur:
        if (info[0],info[1]) not in res:
            res.append((info[0],info[1]))
    return res

#Fonction qui renvoit les deux matrices TFIDF et COUNT
#Ces matrices contiennent les données de chaque personnage (ligne)
#Les données à chaque question (colonne)
#Les réponses sont stockées sous la forme : Oui -> rang pair
#                                           Non -> rang impair
def tfidf_and_count(vecteur,question,item):
    tfidf = [-1]*2*len(vecteur)
    count = [-1]*2*len(vecteur)
    for i in range(len(vecteur)):
        if vecteur[i][4] == None:
            tfidf[2*i] = 0
        else:
            tfidf[2*i] = vecteur[i][4]
        if vecteur[i][5] == None:
            tfidf[(2*i)+1] = 0
        else:
            tfidf[(2*i)+1] = vecteur[i][5]
        if vecteur[i][6] == None:
            count[2*i] = 0
        else:
            count[2*i] = vecteur[i][6]
        if vecteur[i][7] == None:
            count[(2*i)+1] = 0
        else:
            count[(2*i)+1] = vecteur[i][7]
    tfidf = np.array(tfidf).reshape(len(item),2*len(question))
    count = np.array(count).reshape(len(item),2*len(question))
    return tfidf,count

if __name__ == '__main__':
    #On se connecte à la base de données
    base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')
    curseur = base.cursor()
    #On extrait chaque tables, les details sont en haut
    app_tree = extrait_app_tree(curseur)
    vecteur = vector(curseur)
    #Question contient l'ordre des colonnes des questions de la matrice sous la forme [ID, Title]
    question = questionByOrder(vecteur)
    #Item contient l'ordre des lignes des personnages sous la forme [ID, Name]
    item = itemByOrder(vecteur)
    #TFIDF/COUNT sont deux matrices content les TFIDF/COUNT de chaque personnage sous la forme : M[PERSO/QUESTION] = YES, M[PERSO/QUESTION + 1] = NO
    tfidf,count = tfidf_and_count(vecteur,question,item)
    proxi(tfidf)
    #On elague larbre ternaire en arbre binaire
    """app_tree = createBinarytree(app_tree)
    #Preparation de liste_questions pour creer une matrice tfidf_oui,non pour chaque (perso,question)
    ecrireFinal = elagagePerso(app_tree[0],app_tree,tfidf,count,question,item,"")
    file = "../Web/Arbre_Binaire/script/data.js"
    ecriture = open(file,"w",encoding="utf-8")
    ecriture.write("chart_config = { chart : {container: '#tree', scrollbar: 'native', \nconnectors: { type: 'step' },\n node: { HTMLclass: 'nodeExample1' },\n "+
                        "animation: { nodeAnimation: "+'"'+"easeOutBounce"+'"'+", nodeSpeed: 700,connectorsAnimation: "+'"'+"bounce"+'"'+", connectorsSpeed: 700 }},\n"+
                        "nodeStructure : {")
    
    ecriture.write(ecrireFinal)
    ecriture.write(" } \n };")
    ecriture.close
    print("end\n")"""
    
