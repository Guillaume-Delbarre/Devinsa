# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics import pairwise_distances
import math


medoids = None
df = pd.read_csv("../Donnees/classif.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')


def printQuestionCarac(nbCluster=6,nbQuestion=14, nbMedoid=4):
    global df
    dfFile = pd.DataFrame(tableQuest(nbCluster=nbCluster,nbQuestion=nbQuestion, nbMedoid=nbMedoid))
    dfFile.to_csv("../Donnees/infoClusters.csv", mode='w', index=False)

    

def tableQuest(nbCluster=6, nbQuestion=14, nbMedoid=4):
    global df
    agg = sommesClusters(6)
    agg = agg.T
    col=[i for i in range(nbQuestion+int(nbMedoid/2))]
    idx=[]
    
    for i in range(nbCluster):
        count = len(df[df["Clusters"]==i])
        idx.append("Groupe "+str(i))
        idx.append(str(count)+" personnages")
    

    dfFile=pd.DataFrame(index=idx,columns=col)
    for i in range(nbCluster):
        count = len(df[df["Clusters"]==i])
        aggTrie = agg.reindex(agg[i].abs().sort_values(ascending=False).index)
        j=0
        k=0
        questpos=[]
        scorepos=[]
        questneg=[]
        scoreneg=[]
        medoid=persoExtremes(i,medoid=True,nbPerso=nbMedoid)
        for l in range(int(nbMedoid/2)):
            questpos.append(medoid[2*l])
            scorepos.append(medoid[2*l+1])
        while((j+k)<nbQuestion):
            for index,row in aggTrie.iterrows():
                if(j<math.ceil(nbQuestion/2) and row[i]>=0):
                    ind=index.replace("\n","")
                    ind=ind.replace('"','')
                    questpos.append(str(ind))
                    scorepos.append(round(row[i]/count, 2))
                    j+=1
                elif(k<int(nbQuestion/2) and row[i]<0):
                    ind=index.replace("\n","")
                    ind=ind.replace('"','')
                    questneg.append(str(ind))
                    scoreneg.append(round(row[i]/count, 3))
                    k+=1
        quest=questpos+questneg
        score=scorepos+scoreneg
        dfFile.loc["Groupe "+str(i)]=quest
        dfFile.loc[str(count)+" personnages"]=score
    idex = [i for i in range(2*nbCluster)]   
    dfFile = dfFile.set_index([pd.Index(idex),pd.Index(idx)]) 
    dfFile=dfFile.T  
    print(dfFile) 
    return dfFile


def sommesClusters(nbCluster=6, versionConcat=True): #retourne un tableau (nbCluster,nbQuestion) des moyennes par question
    global df
    somme = df.sort_values(by='Clusters')
    #On fait la somme des TF-IDF pour chaque question par cluster 
    somme = pd.DataFrame(somme.groupby(['Clusters'],as_index=False).sum())
    del somme["Clusters"]
    if(not(versionConcat)):
        return somme
    file_question = open("../Donnees/QuestionsLigne.txt","r", encoding='utf-8')
    question = file_question.readlines()
    file_question.close()
    som = pd.DataFrame(index=somme.index,columns=question[1:]) # som (nbCluster x nbQuestion) = +reponseOui - reponseNon
    for i in range(len(question)-1):
        som.iloc[:,i] = somme.iloc[:,2*i]
        som.iloc[:,i] = som.iloc[:,i] - somme.iloc[:,2*i+1] 
    return som


def persoExtremes(numCluster, metric='cosine', medoid=True, nbPerso=4): # Retourne la liste des personnage du cluster dans l'ordre des plus distants
    
    moy = sommesClusters(versionConcat=False)
    moy.fillna(0, inplace=True)
    moy = moy[moy.index==numCluster]
    persoCluster = df[df['Clusters']==numCluster].copy()
    res = pd.DataFrame(pairwise_distances(moy,persoCluster.iloc[0:len(persoCluster.index), 0:len(moy.columns)], metric))
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
            if(i==nbPerso):
                break
    return listePerso

if __name__ == '__main__':
    if (len(sys.argv) == 3):
        numberOfClusters=int(sys.argv[1])
        nbQuestion=int(sys.argv[2])
        printQuestionCarac(numberOfClusters, nbQuestion)
    else:
        #printQuestionCarac(4)
        tableQuest(4,13)