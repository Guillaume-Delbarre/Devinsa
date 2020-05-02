import pandas as pd
import numpy as np
import sys
import time
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

def classHierarchique(n=0) :
    df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')
    #print(df)

    #plus la distance threshold est faible, plus le nombre de cluster est élevé
    if (n==0):  
        clt = AgglomerativeClustering(n_clusters=None,distance_threshold=100,compute_full_tree=True).fit(df)
    else:
        clt = AgglomerativeClustering(n_clusters=n,compute_full_tree=True).fit(df)
    '''
    file = open("../Donnees/testCAH.txt","w")
    for s in clt.labels_ :
        file.write(str(s) + '\n')
    file.close
    '''
    #print(clt.labels_)
    ecritcluster(clt.labels_)
  


def ecritcluster(tabCluster):
    fileentree = open("../Donnees/Personnages.csv","r",encoding='utf-8')
    filesortie = open("../Donnees/kmeans.csv","w",encoding='utf-8')
    taille = len(tabCluster)
    i=-1
    for line in fileentree:
        if (i<taille) :
            if (i<0) :
                filesortie.write(line.replace("\n","") + ";Clusters\n")
            else :
                filesortie.write(line.replace("\n","") + ";" + str(tabCluster[i]) + "\n")
        i += 1

#classHierarchique()

if __name__ == '__main__':
    if (len(sys.argv) == 3):
        numberOfClusters=int(sys.argv[1])
        nbQuestion=int(sys.argv[2])
        classHierarchique(numberOfClusters)
    else:
        classHierarchique(4)