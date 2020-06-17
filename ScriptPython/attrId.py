import pandas as pd 
import os

def attr() :

    fileName = open("../Donnees/name.csv","r", encoding='utf-8')
    listValNom = fileName.readlines()
    fileName.close()

    del listValNom[0]
    data = []
    indexeur = []
    for line in listValNom :
        tab = line.split(',')
        if len(tab) > 2 :
            dernier = tab[len(tab) - 1]
            nom = ""
            for i in range(0,len(tab) - 2) :
                nom += tab[i] + ','
            nom += tab[len(tab) - 2]
        else :
            dernier = tab[1]
            nom = tab[0]
        data.append(nom)
        indexeur.append(dernier)

    df = pd.DataFrame(data, index=indexeur, columns = ['nom'])

    file_nom_id = open("../Donnees/resVisualisation.csv","r",encoding='utf-8')
    listRes = file_nom_id.readlines()
    file_nom_id.close()

    file_zero = open("../Donnees/resVisualisation.csv","w",encoding='utf-8')
    file_zero.write("Axe_X,Axe_Y,id,Cluster,Name\n")
    file_zero.close()

    file = open("../Donnees/resVisualisation.csv","a",encoding="utf-8")
    del listRes[0]
    for l in listRes :
        l = l.replace('\n','')
        elem = l.split(',')
        name = ""
        for i in range(2,len(elem)-1):
            name += elem[i]
        name = name.replace('"','')
        file.write(l + ',' + str(df.loc[name,'nom']))

    file.close()

if __name__ == '__main__':
    attr()