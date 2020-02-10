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

def ecritcluster(listMedoid):
    global y_kmeans10
    fileentree = open("../Donnees/Personnages.csv","r")
    filesortie = open("../Donnees/kmeans.csv","w")
    i=-1
    j=0
    for line in fileentree:
        if (i<1429):
            if (i<0):
                filesortie.write(line.replace("\n","") + ";Clusters;Medoid\n")
            else:
                if i in listMedoid :
                    filesortie.write(line.replace("\n","") + ";" + str(y_kmeans10[i]) + ";1\n")
                    print(i)
                else :
                    filesortie.write(line.replace("\n","") + ";" + str(y_kmeans10[i]) + ";0\n")
        i += 1
    
    fileentree.close()
    filesortie.close()

def ecritTableMed(nbCluster, listMedoid) :
    file = open("../Donnees/clusters.csv","w")
    file.write("Cluster,Personage Médoid,Principale Question\n")

    for i in range(0,nbCluster) :
        nom = nomPerso(i, listMedoid)
        file.write("Groupe " + str(i) + "," + nom + ",\n")
    
    file.close

def nomPerso(n, list) :
    fileentree = open("../Donnees/Personnages.csv","r")
    i=-1
    for line in fileentree :
        if i == n :
            x = line.split(';')
            return x[0]
        i += 1
    
    fileentree.close

def medoid(matrice, clusters, nbCluster):
    i=0
    medoids = [0]*nbCluster
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

def kmeansAlgo(n):
    
    global y_kmeans10
    # Faire le clustering
    df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
    kmeans10 = KMeans(n_clusters=n)
    #Clusters par item
    y_kmeans10 = kmeans10.fit_predict(df)
    
    #Matrice distance au centre ?
    matrice = kmeans10.fit_transform(df)
    
    #print(y_kmeans10)
    listemedoid = medoid(matrice, y_kmeans10, n)
    print(listemedoid)

    ecritcluster(listemedoid)

    ecritTableMed(n, listemedoid)

    
if __name__ == '__main__':
    kmeansAlgo()
    

"""
#Tests
m_clusters = kmeans10.fit(df).labels_.tolist()
centers = np.array(kmeans10.cluster_centers_)
#x = df.iloc[:, 1:].values
"""