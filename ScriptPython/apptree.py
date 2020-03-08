# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:32:09 2020

@author: nathl and OUGO
"""

from InfoArbre import *

def ecrirejstree(resultat, filesortie):
    ecriture = open(filesortie,"w",encoding="utf-8")
    ecriture.write("questionid_1 = {text: { name: '"+resultat[0][0]+"' }, collapsed : true};\n")
    chart_config = "chart_config = [\n{container: '#basic-example',\nconnectors: { type: 'step' },\n node: { HTMLclass: 'nodeExample1' },\n animation: { nodeAnimation: "+'"'+"easeOutBounce"+'"'+", nodeSpeed: 700,connectorsAnimation: "+'"'+"bounce"+'"'+", connectorsSpeed: 700 }},\n questionid_1,"
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
            chart_config += "questionid_"+fils[2]+",\n"
            ecriture.write("questionid_"+fils[2]+" = {parent: questionid_"+parentid+",text: { name: 'Choix : "+choix+"', desc : 'Titre : "+titre+"' }, collapsed : true};\n")
    chart_config = chart_config[0:len(chart_config)-2]
    chart_config += "];"
    ecriture.write(chart_config)
    ecriture.close

def persoRestant(idquestion,elagage):
    for i in range(len(elagage)):
        if(idquestion==elagage[i][0]):
            return elagage[i]
    return -1

def ecrirejstreeV2(resultat,perso,filesortie):
    ecriture = open(filesortie,"w",encoding="utf-8")
    elagage = elagagePerso(resultat[0],resultat,perso,[])
    ecriture.write("questionid_1 = {text: { name: '"+resultat[0][0]+"', desc : 'Personnages restants : "+str(elagage[0][1])+" Personnage médian :"+str(elagage[0][2])+"' }, collapsed : true};\n")
    chart_config = "chart_config = [\n{container: '#basic-example',\nconnectors: { type: 'step' },\n node: { HTMLclass: 'nodeExample1' },\n animation: { nodeAnimation: "+'"'+"easeOutBounce"+'"'+", nodeSpeed: 700,connectorsAnimation: "+'"'+"bounce"+'"'+", connectorsSpeed: 700 }},\n questionid_1,"
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
            chart_config += "questionid_"+fils[2]+",\n"
            info = persoRestant(fils[2],elagage)
            rest = info[1]
            median = guillemet(info[2])
            ecriture.write("questionid_"+fils[2]+" = {parent: questionid_"+parentid+",text: { name: 'Choix : "+choix+"', desc : 'Titre : "+titre+" Personnages restants : "+str(rest)+" Personnage médian :"+str(median)+"'}, collapsed : true};\n")
    chart_config = chart_config[0:len(chart_config)-2]
    chart_config += "];"
    ecriture.write(chart_config)
    ecriture.close

# Main       
arbre = createBinarytree("../Donnees/Arbre.csv")
perso = extraitMatricePersonnage("../Donnees/Personnages.csv")
#print(resultat)
ecrirejstreeV2(arbre,perso,"../Donnees/TreeJS.js")
ecrirejstreeV2(arbre,perso,"../Arbre_Binaire/Treejavascript.js")
