# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, cdist
import os

medoids = None
df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')


def printQuestionCarac(nbCluster=6,nbQuestion=15):
    global df
    file = open("../Donnees/infoClusters.csv","w",encoding='utf-8')
    agg = moyennesClusters()
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

    #écriture des questions caract
    agg_tab=[]
    for i in range(nbCluster):
        agg_tab.append(agg.sort_values(by=i, axis=1, ascending=False).columns)
    
    for j in range(nbQuestion):
        for i in range(nbCluster-1):
            #print(agg_tab[i])
            file.write(agg_tab[i][j]+',')
        file.write(agg_tab[nbCluster-1][j] + '\n')



def moyennesClusters(nbCluster=6): #retourne un tableau (nbCluster,902) des moyennes par question
    global df
    moy = df.sort_values(by='Clusters')
    
    del moy['Medoid']
    #Au lieu d'aller de 0 à 5, les clusters iront de 1 à 6
    for k in range(nbCluster,0,-1):
        moy['Clusters'].replace(k-1,k, inplace=True)
    #On remplace les 0 (absence de donnees) par NaN
    moy = moy.replace(0,np.nan)
    #On fait la moyenne des TF-IDF pour chaque question par cluster (en ignorant les NaN)
    moy = pd.DataFrame(moy.groupby(['Clusters'],as_index=False).mean())
    del moy["Clusters"]
    return moy

    

if __name__ == '__main__':
    printQuestionCarac()
    