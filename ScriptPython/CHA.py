import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

def classHierarchique(n=0) :
    df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')
    print(df['Noms'])

    clt = AgglomerativeClustering(n_clusters=5).fit(df)

    file = open("../Donnees/testCAH.txt","w")
    for s in clt.labels_ :
        file.write(str(s) + '\n')
    file.close
    print(clt.labels_)

def findMedoid(data,listClust,nbClust):
    tabMed = []
    for i in range(nbClust):
        for j in range(len(listClust)):
            print()



def ecritcluster(tabCluster,listMedoid):
    fileentree = open("../Donnees/Personnages.csv","r",encoding='utf-8')
    filesortie = open("../Donnees/kmeans.csv","w",encoding='utf-8')

    taille = len(tabCluster)
    i=-1

    for line in fileentree:
        if (i<taille) :
            if (i<0) :
                filesortie.write(line.replace("\n","") + ";Clusters;Medoid\n")
            else :
                if i in listMedoid :
                    filesortie.write(line.replace("\n","") + ";" + str(tabCluster[i]) + ";1\n")
                    #print(i)
                else :
                    filesortie.write(line.replace("\n","") + ";" + str(tabCluster[i]) + ";0\n")
        i += 1

classHierarchique()