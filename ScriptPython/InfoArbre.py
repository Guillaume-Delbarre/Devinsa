# -*- coding: utf-8 -*-
"""
Created on Wed Jan  04 14:32:09 2020

@author: OUGO
"""

def extraitMatricePersonnage(file):
    results = []
    with open(file,encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            results.append(row)
    return results

def getfils(resultat, parentid):
    res = []
    for questions in resultat:
        if (questions[3]== str(parentid)):
            res.append([questions[1],questions[0],questions[2]])
    return res
            
def createBinarytree(file):  
    file = open(file,"r",encoding="utf-8")
    resultat = []
    temp = []
    exclus = []
    i = 0
    for line in file:
        if (i>0):
            temp = line.split(",")
            if (temp[1] == 'p' or temp[3] in exclus):
                exclus.append(temp[2])
            else:
                i=0
                for item in temp:
                    temp[i] = item.replace('\n','').replace('\\N','')
                    i+=1
                resultat.append([temp[0],temp[1],temp[2],temp[3]])
        i +=1
    return resultat

def avoirRangQuestion(question,matricePersoQuestion):          
    for i in range(len(matricePersoQuestion[0])):       
        if(question==matricePersoQuestion[0][i][4:]):
            return i
    return -1

def obtenirRangQuestionsFilles(parentid,matriceQuestion):
    verif = 0
    res = []
    for i in range(len(matriceQuestion)):
        if(matriceQuestion[i][3]==parentid):
            res.append(i)
            verif += 1
        if (verif==2):
            return res
    return -1

def recopieMatrice(matrice):
    reponse = []
    for i in range(len(matrice)):
        reponse.append(matrice[i])
    return reponse

def compterPerso(rangQuestion,matricePerso):
    res = recopieMatrice(matricePerso)
    for i in range(1,len(matricePerso)):
        idf = matricePerso[i][rangQuestion]
        if(float(idf)<TAUX):
            res.remove(matricePerso[i])
    return res

def median(matrice):
    med = [0]
    summ = 0
    for j in range(1,len(matrice[0])):
        for i in range(1,len(matrice)):
           summ += float(matrice[i][j])
        summ = summ/(len(matrice)-1)
        med.append(summ)
        summ = 0
    return med

def proxi(med,matrice):
    dist_aux = 0
    for j in range(1,len(matrice[0])):
        dist_aux += carre(med[j]-float(matrice[1][j]))
    dist = dist_aux
    dist_aux = 0
    rang = 1
    for i in range(2,len(matrice)):
        for j in range(2,len(matrice[0])):
            dist_aux += carre(med[j]-float(matrice[i][j]))
        if(dist_aux<dist):
            dist = dist_aux
            rang = i
        dist_aux = 0
    return rang

def carre(x):
    return (x)*(x)

def guillemet(s):
    i = 0
    taille = len(s)
    while(i<taille):
        if(s[i]=="'"):
            s = s[:i]+"'+"+s[i:]
            i += 2
        i+=1
    return s
                    
def elagagePerso(question,matriceArbre,matricePerso,res):
    if(len(matricePerso)==1):
        res.append([question[2],0,'Aucun'])
    else:
        rangMedian = proxi(median(matricePerso),matricePerso)
        res.append([question[2],len(matricePerso)-1,matricePerso[rangMedian][0]])
    rangQuestionsFilles = obtenirRangQuestionsFilles(question[2],matriceArbre)
    if(rangQuestionsFilles==-1):
        return
    rangQuestion = avoirRangQuestion(question[0],matricePerso)
    if(rangQuestion==-1):
        print("Error 2")
        return
    choixOui = rangQuestionsFilles[0]
    choixNon = rangQuestionsFilles[1]
    rangQuestionOui = avoirRangQuestion(matriceArbre[choixOui][0],matricePerso)
    rangQuestionNon = avoirRangQuestion(matriceArbre[choixNon][0],matricePerso)
    matricePersoOui = compterPerso(rangQuestion, matricePerso)
    matricePersoNon = compterPerso(rangQuestion+1, matricePerso)
    elagagePerso(matriceArbre[choixNon],matriceArbre,matricePersoNon,res)
    elagagePerso(matriceArbre[choixOui],matriceArbre,matricePersoOui,res)
    return res



