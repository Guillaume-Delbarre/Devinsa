# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from questionsCaracteristiques import moyennesClusters
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
    


def differenceFromCluster(perso):
    # On recupere le tableau des moyennes par question et par cluster et le tableau du perso
    moy = moyennesClusters()
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
    for i in range(len(df.index)):
        name = df.iloc[[i]].index[0]
        file.write(name+',')
        questionPerso = differenceFromCluster(name)
        for j in range(nbQuestion):
            file.write(questionPerso[j]+',')
        file.write(questionPerso[nbQuestion]+'\n')
    
    

def persoDistants(numCluster, metric='cosine'): # Retourne la liste des personnage du cluster dans l'ordre des plus distants
    moy = moyennesClusters()
    moy.fillna(0, inplace=True)
    moy = moy[moy.index==numCluster]
    persoCluster = df.copy()
    persoCluster = persoCluster[persoCluster['Clusters']==numCluster]
    res = pd.DataFrame(pairwise_distances(moy,persoCluster.iloc[0:len(persoCluster.index), 0:902], metric))
    res.sort_values(by=0,axis=1, inplace=True, ascending=False)
    res= res.T
    listePerso = []
    for index, row in res.iterrows():
        listePerso.append(persoCluster.iloc[[index]].index[0])
    print(listePerso)
    return listePerso


    
def printPersoDistants(nbCluster=6,nbPerso=10, metric='cosine'):
    global df
    file = open("../Donnees/persoDistants.csv","w",encoding='utf-8')
    for i in range(nbCluster):
        listePerso = persoDistants(i,metric)
        file.write(str(i)+',')
        for j in range(nbPerso):
            file.write(listePerso[j]+',')
        file.write(listePerso[nbPerso]+'\n')







if __name__ == '__main__':
    differenceFromCluster("Abel Jabri")