import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

def classHierarchique(n=0) :
    df = pd.read_csv("Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')
    #print(df)

    clt = AgglomerativeClustering(n_clusters=5).fit(df)

    file = open("Donnees/testCAH.txt","w")
    for s in clt.labels_ :
        file.write(str(s) + '\n')
    file.close
    print(clt.labels_)


classHierarchique()