import os

global listeParNom
global listeNoms

file = open("test_des_res.csv","w")

file.close()

listeParNom = []
listeNoms = []

def ecritStringFichier(list) :
    file_ecrit = open("test_des_res.csv","a")
    
    os.chmod("test_des_res.csv", 0o777)
    
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
            
        #print(listeNoms)
        
    else :
        
        
        listeParNom.append(new[1])
        
        clean = new[2].replace('\n','')
        listeParNom.append(clean)
        
        #print(listeParNom)
    
def compteNBQuestion() :
    
    file_question = open("resquestion.txt","r")
    compt = 0
    f_line = file_question.readlines()
    
    for li in f_line :
        compt = compt + 1
    
    return compt


listetitre = ["Noms"]
nbQuestion = compteNBQuestion()

for i in range(0,nbQuestion-1) :
    listetitre.append("Oui" + str(i))
    listetitre.append("Non" + str(i))

ecritStringFichier(listetitre)



file_res = open("resdatatot.txt","r")


f1 = file_res.readlines()

for x in f1 :
        
        y = x.replace('\\N','0')
        manip(y)
        
file_res.close() 

