# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
from sklearn.metrics import pairwise_distances


medoids = None
df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')


def printQuestionCarac(nbCluster=6,nbQuestion=14):
    global df
    if(nbQuestion % 2)!=0:
        raise ValueError("Veuillez entrer un nombre pair de questions")
    dfFile = tableQuest(nbCluster=nbCluster,nbQuestion=nbQuestion)
    #df.sort_values(by='Clusters', inplace=True)
    #On récupère les médoides dans un tableau
    #medoids = df.loc[df['Medoid']==1].index.values
    
    dfFile.to_csv("../Donnees/infoClusters.csv", mode='w')

    
    


def tableQuest(nbCluster=6, nbQuestion=14, nbMedoid=4):
    global df
    agg = sommesClusters()
    agg = agg.T
    col=[i for i in range(nbQuestion)]
    idx=[]
    
    for i in range(nbCluster):
        count = len(df[df["Clusters"]==i])
        idx.append("Groupe "+str(i))
        idx.append(str(count)+" personnages")
    for i in range(nbCluster):
             medoid=persoExtremes(i,medoid=True,nbPerso=4)
             print(medoid)

    dfFile=pd.DataFrame(index=idx,columns=col)
    for i in range(nbCluster):
        count = len(df[df["Clusters"]==i])
        aggTrie = agg.reindex(agg[i].abs().sort_values(ascending=False).index)
        j=0
        k=0
        quest=[]
        score=[]
        while((j+k)<nbQuestion):
            for index,row in aggTrie.iterrows():
                if(j<(nbQuestion/2) and row[i]>=0):
                    ind=index.replace("\n","")
                    ind=ind.replace('"','')
                    quest.append(str(ind))
                    score.append(row[i])
                    j+=1
                elif(k<(nbQuestion/2) and row[i]<0):
                    ind=index.replace("\n","")
                    ind=ind.replace('"','')
                    quest.append(str(ind))
                    score.append(row[i])
                    k+=1
        dfFile.loc["Groupe "+str(i)]=quest
        dfFile.loc[str(count)+" personnages"]=score

    dfFile=dfFile.T
    return dfFile

def sommesClusters(nbCluster=6, versionConcat=True): #retourne un tableau (nbCluster,902) des moyennes par question
    global df
    somme = df.sort_values(by='Clusters')
    
    del somme['Medoid']
    #Au lieu d'aller de 0 à 5, les clusters iront de 1 à 6
    for k in range(nbCluster,0,-1):
        somme['Clusters'].replace(k-1,k, inplace=True)
    #On fait la somme des TF-IDF pour chaque question par cluster 
    somme = pd.DataFrame(somme.groupby(['Clusters'],as_index=False).sum())
    del somme["Clusters"]
    if(not(versionConcat)):
        return somme
    file_question = open("../Donnees/QuestionsLigne.txt","r", encoding='utf-8')
    question = file_question.readlines()
    file_question.close()
    som = pd.DataFrame(index=somme.index,columns=question) # som (nbCluster x nbQuestion) = +reponseOui - reponseNon
    for i in range(len(question)):
        som.iloc[:,i] = somme.iloc[:,2*i]
        som.iloc[:,i] = som.iloc[:,i] - somme.iloc[:,2*i+1]
    return som

def persoExtremes(numCluster, metric='cosine', medoid=True, nbPerso=4): # Retourne la liste des personnage du cluster dans l'ordre des plus distants
    moy = sommesClusters(versionConcat=False)
    moy.fillna(0, inplace=True)
    moy = moy[moy.index==numCluster]
    persoCluster = df[df['Clusters']==numCluster].copy()
    res = pd.DataFrame(pairwise_distances(moy,persoCluster.iloc[0:len(persoCluster.index), 0:902], metric))
    if medoid:
        res.sort_values(by=0,axis=1, inplace=True)
    else :
        res.sort_values(by=0,axis=1, inplace=False)
    res= res.T
    listePerso = []
    i=0
    
    for index, row in res.iterrows():
            listePerso.append(persoCluster.iloc[[index]].index[0])
            i+=1
            if(i>nbPerso):
                break
    print(listePerso)
    return listePerso

if __name__ == '__main__':
    persoExtremes(0)