# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from questionsCaracteristiques import moyennesClusters

df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')

def questionCaracPerso(perso):
    global df
    cluster = df.loc[perso,'Clusters']
    medoid = df.loc[perso,'Medoid']
    del df['Medoid']
    del df['Clusters']
    questionPerso = df.loc[[perso]].sort_values(by=perso,axis=1,ascending=False)
    
    if(medoid):
        questionPerso.insert(0,'Medoid','Oui')
    else:
        questionPerso.insert(0,'Medoid','Non')

    questionPerso.insert(0,'Cluster',cluster)
    
    return questionPerso
    
    #print(questionPerso)


def difference(dfPerso):
    moy = moyennesClusters()
    


if __name__ == '__main__':
    questionCaracPerso("Abel Jabri")

