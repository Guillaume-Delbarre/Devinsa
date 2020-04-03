# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

medoids = None
df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')


def printQuestionCarac(nbCluster=6,nbQuestion=4):
    global df
    file = open("../Donnees/infoClusters.csv","w",encoding='utf-8')
    agg = sommesClusters()
    df.sort_values(by='Clusters', inplace=True)
    #On récupère les médoides dans un tableau
    medoids = df.loc[df['Medoid']==1].index.values
    #Changement de sens pour le tableau donc pour le csv aussi
    """
    #ecriture de l'entête
    file.write("Cluster,Medoid,")
    for i in range(nbQuestion-1):
        file.write("Q"+str(i)+",")
    file.write("Q"+str(nbQuestion-1)+"\n")

    for i in range(1,nbCluster+1):
        #Pour un cluster donné, on ordonne inversement les question en fonction du score TF-IDF
        agg_sorted = agg.sort_values(by=i, axis=1, ascending=False)
        file.write(str(i-1)+","+medoids[i-1]+",")
        j=0
        for column in agg_sorted.columns:
            if j>=nbQuestion:
                break
            else: 
                file.write(column+",")
            j=j+1
        file.write("\n")
    """

    #Nouvelle manière :

    #écriture de l'entête
    for i in range(nbCluster-1) :
        file.write("Groupe " + str(i) + ',')
    file.write("Groupe " + str(nbCluster-1) + '\n')
    #écriture des médoids
    for i in range(nbCluster-1):
        file.write(medoids[i] + ',')
    file.write(medoids[nbCluster-1] + '\n')
    dfFile=pd.DataFrame()
    #écriture des questions caract
    agg = agg.T
    for i in range(nbCluster):
        count = len(df[df["Clusters"]==i])
        
        aggTrie = agg.reindex(agg[i].abs().sort_values(ascending=False).index)
        j=0
        k=0
        while((j+k)<nbQuestion):
            for index,row in aggTrie.iterrows():
                if(j<(nbQuestion/2+1) ):
                    dfFile[str(i)]=index
                    print(aggTrie.loc[index])
                    dfFile[str(count)]=aggTrie.iloc[[index]].values
                    j+=1
                elif(k<(nbQuestion/2+1)):
                    
                    k+=1


    """
    for j in range(nbQuestion):
        for i in range(nbCluster-1):
            #print(agg_tab[i])
            file.write(agg_tab[i][j]+',')
        file.write(agg_tab[nbCluster-1][j] + '\n')
    """



def sommesClusters(nbCluster=6): #retourne un tableau (nbCluster,902) des moyennes par question
    global df
    somme = df.sort_values(by='Clusters')
    
    del somme['Medoid']
    #Au lieu d'aller de 0 à 5, les clusters iront de 1 à 6
    for k in range(nbCluster,0,-1):
        somme['Clusters'].replace(k-1,k, inplace=True)
    #On fait la somme des TF-IDF pour chaque question par cluster 
    somme = pd.DataFrame(somme.groupby(['Clusters'],as_index=False).sum())
    del somme["Clusters"]
    file_question = open("../Donnees/QuestionsLigne.txt","r", encoding='utf-8')
    question = file_question.readlines()
    file_question.close()
    som = pd.DataFrame(index=somme.index,columns=question) # som (nbCluster x nbQuestion) = +reponseOui - reponseNon
    for i in range(len(question)):
        som.iloc[:,i] = somme.iloc[:,2*i]
        som.iloc[:,i] = som.iloc[:,i] - somme.iloc[:,2*i+1]
    return som

    

if __name__ == '__main__':
    printQuestionCarac()
    