import mysql.connector
import numpy as np

#APP_TREE
#[id,parent_id,choice,question_id,title]
#VECTEUR
#[id_item,name,id_question,title,yes_tfidf,no_tfidf,yes_count,no_count]

base = mysql.connector.connect(host='localhost',database='devinsa',user='root',password='devinsa!')

curseur = base.cursor()

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
            
            

def miseEnFormeText(text):
    return text.replace('\'',"\\'")

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

def HTMLclass(choice):
    if choice=='o':
        return 'light-green'
    if choice=='n':
        return 'light-red'
    return 'None'

def elagagePerso(question,app_tree,tfidf,count,questionOrder,itemOrder,ecrire):
    if(itemOrder.shape[0]==0):        
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
        for question in questionsFilles:
            if question[2]=='o':
                choixOui = question
            elif question[2] =='n':
                choixNon = question
            else:
                print("Error 3")
                return
        rangQuestion = avoirRangQuestion(question[3],questionOrder)
        count_yes,tfidf_yes,itemOrder_yes = compterPerso(rangQuestion,count,tfidf,itemOrder)
        count_no,tfidf_no,itemOrder_no = compterPerso(rangQuestion+1,count,tfidf,itemOrder)
        ecrire += "\n{"
        if (choixOui!=[]):
            ecrire += elagagePerso(choixOui,app_tree,tfidf_yes,count_yes,questionOrder,itemOrder_yes,"")
        ecrire += "\n}, \n {"
        if (choixNon!=[]):
            ecrire += elagagePerso(choixNon,app_tree,tfidf_no,count_no,questionOrder,itemOrder_no,"")
        ecrire += "\n } \n]"
        return ecrire

def proxi(tfidf):
    moyen = np.mean(tfidf,0)
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


def questionByOrder(vecteur):
    res = []
    for info in vecteur:
        if (info[2],info[3]) not in res:
            res.append((info[2],info[3]))
        else:
            return res

def itemByOrder(vecteur):
    res = []
    for info in vecteur:
        if (info[0],info[1]) not in res:
            res.append((info[0],info[1]))
    return res

def personnage(vecteur,question,item):
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

def main(curseur):
    #On extrait chaque tables, les details sont en haut
    app_tree = extrait_app_tree(curseur)
    vecteur = vector(curseur)
    #Question contient l'ordre des colonnes des questions de la matrice sous la forme [ID, Title]
    question = questionByOrder(vecteur)
    #Item contient l'ordre des lignes des personnages sous la forme [ID, Name]
    item = itemByOrder(vecteur)
    #TFIDF/COUNT sont deux matrices content les TFIDF/COUNT de chaque personnage sous la forme : M[PERSO/QUESTION] = YES, M[PERSO/QUESTION + 1] = NO
    tfidf,count = personnage(vecteur,question,item)
    #On elague larbre ternaire en arbre binaire
    app_tree = createBinarytree(app_tree)
    compterPerso(2,count,tfidf,item)
    #Preparation de liste_questions pour creer une matrice tfidf_oui,non pour chaque (perso,question)
    """ecrireFinal = elagagePerso(app_tree[0],app_tree,tfidf,count,question,item,"")
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
