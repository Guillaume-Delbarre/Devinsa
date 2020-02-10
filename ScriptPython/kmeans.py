# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 20:58:52 2020

@author: nathl
"""

import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

def trouveroptimal():
    #Trouver le nombre optimal de clusters
    df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
    x = df.iloc[:, 1:].values
    Error =[]
    for i in range(1, 31):
        kmeans = KMeans(n_clusters = i).fit(x)
        kmeans.fit(x)
        Error.append(kmeans.inertia_)
        
    plt.plot(range(1, 31), Error)
    plt.title('Elbow method')
    plt.xlabel('No of clusters')
    plt.ylabel('Error')
    plt.show()

def ecritcluster():
    global y_kmeans10
    fileentree = open("../Donnees/Personnages.csv","r")
    filesortie = open("../Donnees/kmeans.csv","w")
    i=-1
    for line in fileentree:
        if (i<1429):
            if (i<0):
                filesortie.write(line.replace("\n","") + ";Clusters \n")
                
            else:
                filesortie.write(line.replace("\n","") + ";" + str(y_kmeans10[i]) + "\n")
        i += 1
    
    fileentree.close()
    filesortie.close()
    
def medoid(matrice, clusters,n):
    medoids = [0]*n
    for j in range(0,len(matrice[0])):
        medoids[j] = getmin(matrice,clusters,j)
    return medoids

def getmin(matrice,clusters, numclust):
    curr = 100000000
    medoid = 0
    for i in range(0,len(matrice)):
        val = matrice[i][numclust]
        if (val<curr and clusters[i] == numclust):
            medoid = i
            curr = val 
    return medoid

def kmeansAlgo(n=10):
    
    global y_kmeans10
    # Faire le clustering
    df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
    kmeans10 = KMeans(n_clusters=n)
    #Clusters par item
    y_kmeans10 = kmeans10.fit_predict(df)
    
    #Matrice distance au centre ?
    matrice = kmeans10.fit_transform(df)
    
    ecritcluster()
    #print(y_kmeans10)
    listemedoid = medoid(matrice, y_kmeans10,n)

    
if __name__ == '__main__':
    kmeansAlgo()
    

"""
#Tests
m_clusters = kmeans10.fit(df).labels_.tolist()
centers = np.array(kmeans10.cluster_centers_)
#x = df.iloc[:, 1:].values
"""