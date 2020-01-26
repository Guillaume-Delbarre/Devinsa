# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 20:58:52 2020

@author: nathl
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# Faire le clustering

df = pd.read_csv("Personnages.csv", sep = ";", header=1, encoding = 'latin1')
x = df.iloc[:, 1:].values
kmeans15 = KMeans(n_clusters=15)
y_kmeans15 = kmeans15.fit_predict(x)

#Ecrire le cluster
fileentree = open("Personnages.csv","r")
filesortie = open("kmeans.csv","w")
i=-1
for line in fileentree:
    if (i<1429):
        if (i<0):
            filesortie.write(line.replace("\n","") + ";Clusters \n")
        else:
            filesortie.write(line.replace("\n","") + ";" + str(y_kmeans15[i]) + "\n")
    i += 1

fileentree.close()
filesortie.close()



#Trouver le nombre optimal de clusters
"""
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
"""