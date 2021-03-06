# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from questionsCaracteristiques import sommesClusters, persoExtremes
from scipy.spatial.distance import pdist, cdist
from sklearn.metrics import pairwise_distances

df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')

def questionCaracPerso(perso, sort=False):
    global df
    questionPerso = df.copy(deep=False)
    # On recupere le num cluster et l'info sur le medoid avant de supprimer pour le tri, pour pouvoir rajouter les infos au début
    cluster = questionPerso.loc[perso,'Clusters']
    medoid = questionPerso.loc[perso,'Medoid']
    del questionPerso['Medoid']
    del questionPerso['Clusters']
    # On recupere la ligne correspondant au personnage et on trie selon les questions les plus caracteristiques (TF-IDF plus élevé)
    if(sort):
        questionPerso = questionPerso.loc[[perso]].sort_values(by=perso,axis=1,ascending=False)
    else:
        questionPerso = questionPerso.loc[[perso]]
    # On rajoute les infos sur cluster et medoid
    if(medoid):
        questionPerso.insert(0,'Medoid','Oui')
    else:
        questionPerso.insert(0,'Medoid','Non')
    questionPerso.insert(0,'Cluster',cluster)
    return questionPerso
    

"""
def differenceFromCluster(perso):
    # On recupere le tableau des moyennes par question et par cluster et le tableau du perso
    moy = sommesClusters()
    questionPerso = questionCaracPerso(perso, sort=False)
    # On recupere le numero de cluster du personnage
    numCluster = questionPerso["Cluster"].values[0]
    # On garde les moyennes par question du cluster correspondant
    moy = moy[moy.index==numCluster]
    moy.fillna(0, inplace=True)
    del questionPerso['Cluster']
    del questionPerso['Medoid']
    res = pd.DataFrame(np.absolute(np.array(moy) - np.array(questionPerso)))
    res.sort_values(by=0, axis=1,ascending=False, inplace=True)
    res=res.T
    questionPerso=questionPerso.T 
    listeQuestions = []
    for index, row in res.iterrows(): 
        listeQuestions.append(questionPerso.iloc[[index]].index[0]) 
    return listeQuestions

def printQuestionDiffCluster(nbQuestion=10):
    global df
    file = open("../Donnees/questionDiffCluster.csv","w",encoding='utf-8')
    file.write("Personnage,")
    for i in range(nbQuestion):
        file.write("Q"+str(i)+',')
    file.write("Q"+str(nbQuestion)+'\n')
    for i in range(len(df.index)):
        name = df.iloc[[i]].index[0]
        file.write(name+',')
        questionPerso = differenceFromCluster(name)
        for j in range(nbQuestion):
            file.write(questionPerso[j]+',')
        file.write(questionPerso[nbQuestion]+'\n')
"""
    




    
def printPersoDistants(nbCluster=6,nbPerso=10, metric='cosine'):
    global df
    idx=[i for i in range(nbCluster)]
    col = [i for i in range(nbPerso)]
    dfPerso = pd.DataFrame(index=idx,columns=col)
    for i in range(nbCluster):
        listePerso = persoExtremes(i,metric, medoid=False, nbPerso=nbPerso)
        dfPerso.iloc[i]=listePerso
    dfPerso=dfPerso.T
    dfPerso.to_csv("../Donnees/persoDistants.csv",index=False)







if __name__ == '__main__':
    printPersoDistants()