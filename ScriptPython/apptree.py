# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:32:09 2020

@author: nathl
"""

def getfils(resultat, parentid):
    res = []
    for questions in resultat:
        if (questions[3]== str(parentid)):
            res.append([questions[1],questions[0],questions[2]])
    return res
            
def createBinarytree(file):  
    file = open(file,"r")
    resultat = []
    temp = []
    exclus = []
    for line in file:
        temp = line.split(",")
        if (temp[1] == 'p' or temp[4] in exclus):
            exclus.append(temp[3])
        else:
            i=0
            for item in temp:
                temp[i] = item.replace('\n','').replace('\\N','')
                i+=1
            resultat.append([temp[0],temp[1],temp[3],temp[4]])
    return resultat

def ecrirejstree(resultat, filesortie):
    ecriture = open(filesortie,"w")
    ecriture.write("config = {container: '#tree-simple'};\n")
    ecriture.write("questionid_1 = {text: { name: '"+resultat[0][0]+"' }};\n") 
    for questions in resultat:   
        parentid = questions[2]
        touslesfils = getfils(resultat, parentid)
        #print(touslesfils)
        for fils in touslesfils:            
            if fils[0] == 'o' :
                choix = "Oui"
            else :
                choix = "Non"
            titre = fils[1]
            #print(fils)
            ecriture.write("questionid_"+fils[2]+" = {parent: questionid_"+parentid+",text: { name: 'Choix : "+choix+" || Titre : "+titre+"' }};\n")
    ecriture.close

# Main       

resultat = createBinarytree("tree.txt")
print(resultat)
ecrirejstree(resultat,"resultat.txt")