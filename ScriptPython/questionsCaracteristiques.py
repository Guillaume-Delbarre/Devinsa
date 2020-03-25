# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, cdist

medoids = None


def ecritQuestionCarac(df,agg,nbCluster,nbQuestion):
    file = open("Donnees/infoClusters.csv","w",encoding='utf-8')
    
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
    for i in range(1,nbCluster+1) :
        file.write(str(i) + ',')
    #file.write(nbCluster+1 + '\n')

    #écriture des médoids
    for i in range(nbCluster):
        file.write(medoid[i])
    #file.write(medoid[nbCluster])

    #écriture des questions caract
    agg_tab=[]
    for i in range(1,nbCluster+1):
        agg_tab.append(agg.sort_values(by=i, axis=1, ascending=False))
    
    for j in range(nbQuestion):
        for i in range(nbCluster):
            file.write(agg_tab[i][j]+',')
        file.write('\n')


def getQCarac(nbCluster=6, nbQuestion=5):
    global medoids
    df = pd.read_csv("Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')
    df.sort_values(by='Clusters', inplace=True)
    #On récupère les médoides dans un tableau
    medoids = df.loc[df['Medoid']==1].index.values
    
    del df['Medoid']
    #Au lieu d'aller de 0 à 5, les clusters iront de 1 à 6
    for k in range(nbCluster,0,-1):
        df['Clusters'].replace(k-1,k, inplace=True)
    #On remplace les 0 (absence de donnees) par NaN
    df = df.replace(0,np.nan)
    #On fait la moyenne des TF-IDF pour chaque question par cluster (en ignorant les NaN)
    agg = df.groupby(['Clusters']).mean()
    #print(cdist(agg[agg.index==1],df[df['Clusters']==1].iloc[0:82,0:902])) Probleme avec les NaN
    ecritQuestionCarac(df,agg,nbCluster,nbQuestion)
    
    

if __name__ == '__main__':
    getQCarac()
    