# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics import pairwise_distances
import re
from questionsCaracteristiques import sommesClusters

df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')
file_question = open("../Donnees/QuestionsLigne.txt","r", encoding='utf-8')
question = file_question.readlines()
question = [w.replace('\n',"") for w in question]
file_question.close()

# Fonction traitement dans le cas d'un cluster
def cluster(i):
    global df
    global question
    somme = pd.DataFrame(df.groupby(['Clusters'],as_index=False).sum())
    somme = pd.DataFrame(somme[somme["Clusters"]==i], copy=True)
    del somme["Clusters"]
    som = pd.DataFrame(index=pd.Index([i]),columns=question[1:])
    for j in range(len(question)-1):
        som.iloc[0,j] = somme.iloc[0,2*j]
        som.iloc[0,j] = som.iloc[0,j] - somme.iloc[0,2*j+1] 

    count = len(df[df["Clusters"]==i])
    som = som/count
    return som

#fonction traitement dans le cas d'une sélection
def selection(L):
    global df 
    global question
    somme = pd.DataFrame(pd.DataFrame(df.loc[L, :], copy=True).sum())
    somme = somme.T
    del somme["Clusters"]
    som = pd.DataFrame(index=pd.Index([str(L)]),columns=question[1:])
    for i in range(len(question)-1):
        som.iloc[0,i] = somme.iloc[0,2*i]
        som.iloc[0,i] = som.iloc[0,i] - somme.iloc[0,2*i+1] 
    som = som/len(L)
    return som
    


def differences(L1,L2):

    regex = re.compile("Groupe (.)")
    group1 = regex.search(str(L1))
    group2 = regex.search(str(L2))

    # 1er parametre est un cluster
    if group1!=None:
        L1=int(group1.group(1))
        df1 = cluster(L1)
    # 1er parametre est une sélection
    else:
        #Traitement car les string sont interprétés, il faut rajouter les ""
        L1= str(L1).replace("[","").replace("]","")
        L1 = L1.split(",")
        df1 = selection(L1)

    # 2e parametre est un cluster
    if group2!=None:
        L2=int(group2.group(1))
        df2 = cluster(L2)
    # 2e parametre est une sélection
    else:
        #Traitement car les string sont interprétés, il faut rajouter les ""
        L2= str(L2).replace("[","").replace("]","")
        L2 = L2.split(",")
        df2 = selection(L2)
    
    data = df1.merge(df2, how="outer")
    dif = data.diff().iloc[1,:]
    data=data.T 
    data["dif"]=dif
    res = data.reindex(data["dif"].abs().sort_values(ascending = False).index)
    res= res.reset_index()
    res.columns = ["Question","Selection1","Selection2","dif"]
    res = res.round(2)
    res.to_csv("../Donnees/differences.csv", mode='w', index=True)



if __name__ == '__main__':

    if (len(sys.argv) == 3):
        L1=sys.argv[1]
        L2=sys.argv[2]
        differences(L1,L2)

    else:
        raise ValueError("Nombre d'arguments incorrect")
        