import os

global listeParNom
global listeNoms
global listeQuestions

file = open("Personnages2.csv","w")
file.close()

listeParNom = []
listeNoms = []
listeQuestions = []

def ecritStringFichier(list) :
    file_ecrit = open("Personnages2.csv","a")
    
    os.chmod("Personnages2.csv", 0o777)
    
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
    
    if (nb > 3) :
        dernier = new[nb-1]
        penultieme = new[nb-2]
        
        premier = ""
        for i in range(0,nb-2):
            premier = premier + new[i]
        
        new = [premier,penultieme,dernier]

    if(not (new[0] in listeNoms)) :
        
        if (len(listeNoms) > 0) :
            #print(listeParNom)
            ecritStringFichier(listeParNom)
            
            
        listeParNom = []
            
        listeNoms.append(new[0])
        listeParNom.append(new[0])

        if(new[1] == ""):
            new[1] = "0"
        listeParNom.append(new[1])
        
        clean = new[2].replace('\n','')
        if(clean == ""):
            clean = "0"
        listeParNom.append(clean)
            
        #print(listeNoms)
        
    else :
        
        if(new[1] == ""):
            new[1] = "0"
        listeParNom.append(new[1])
        
        clean = new[2].replace('\n','')
        if(clean == ""):
            clean = "0"
        listeParNom.append(clean)
        
        #print(listeParNom)
    
def questionIntoList() :
    
    file_question = open("QuestionsLigne.txt","r")
    f_line = file_question.readlines()
    
    return f_line

listeQ =[]
listetitre = ["Noms"]
file_question = open("QuestionsLigne.txt","r")
listeQ = file_question.readlines()
file_question.close()
for q in listeQ :
    q = q.replace('\n',"")
    q = q.replace('"',"")
    listeQuestions.append(q)
print(listeQuestions)

for i in range(len(listeQuestions)) :
    listetitre.append("Oui " + listeQuestions[i])
    listetitre.append("Non " + listeQuestions[i])

ecritStringFichier(listetitre)




file_res = open("Vecteur.csv","r")
f1 = file_res.readlines()
file_res.close()
del f1[0]
for x in f1 :
        y = x.replace('\\N','0')
        manip(y)
        

        

