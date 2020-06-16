# -*- coding: utf-8 -*-
import os

listeParNom = []
listeNoms = []

def miseEnPage(): 

    file = open("../Donnees/Personnages.csv","w", encoding='utf-8')
    file.close()
    global listeParNom
    global listeNoms
    listeQuestions = []
    listeQ =[]
    listetitre = ["id;Noms"]
    
    #Mettre les questions du fichier dans listeQuestions
    file_question = open("../Donnees/QuestionsLigne.txt","r", encoding='utf-8')
    listeQ = file_question.readlines()
    file_question.close()
    for q in listeQ[1:] :
        q = q.replace('\n',"")
        q = q.replace('"',"")
        listeQuestions.append(q)
    #print(listeQuestions)

    #construction de la 1ere ligne du fichier, dans listetitre
    for i in range(len(listeQuestions)) :
        listetitre.append("Oui" + listeQuestions[i])
        listetitre.append("Non" + listeQuestions[i])
    #ecriture de listetitre dans fichier csv
    ecritStringFichier(listetitre)
    
    file_res = open("../Donnees/Vecteur.csv","r", encoding='utf-8')
    f1 = file_res.readlines()
    file_res.close()
    
    del f1[0]
    for x in f1 :
            y = x.replace('\\N','0')
            manip(y)

def ecritStringFichier(list) :
        file_ecrit = open("../Donnees/Personnages.csv","a",encoding='utf-8')
        string = regroupList(list)
        file_ecrit.write(string)
        file_ecrit.close()

def regroupList(list) :
        fin = ""
        for x in list :
            fin = fin + x + ";"

        fin = fin[0:-1]
        fin = fin + "\n"
        return fin

def manip(s) :
        global listeParNom 
        global listeNoms
        new = s.split(',')
        nb = len(new)
        
        if (nb > 4) :
            dernier = new[nb-1]
            penultieme = new[nb-2]
            premier = new[0]
            deuxieme = ""
            for i in range(0,nb-2):
                deuxieme = deuxieme + new[i]
            new = [premier,deuxieme,penultieme,dernier]

        if(not (new[1] in listeNoms)) :
            
            if (len(listeNoms) > 0) :
                #print(listeParNom)
                ecritStringFichier(listeParNom)
                
                
            listeParNom = []
                
            listeNoms.append(new[1])
            listeParNom.append(new[0])
            listeParNom.append(new[1])

            if(new[2] == ""):
                new[2] = "0"
            listeParNom.append(new[2])
            
            clean = new[3].replace('\n','')
            if(clean == ""):
                clean = "0"
            listeParNom.append(clean)
                
            #print(listeNoms)
            
        else :
            
            if(new[2] == ""):
                new[2] = "0"
            listeParNom.append(new[2])
            
            clean = new[3].replace('\n','')
            if(clean == ""):
                clean = "0"
            listeParNom.append(clean)
            
            #print(listeParNom)

if __name__ == '__main__':
    miseEnPage()       
        

