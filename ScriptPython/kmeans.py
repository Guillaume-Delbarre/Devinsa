# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 20:58:52 2020

@author: nathl
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# Faire le clustering
df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
kmeans10 = KMeans(n_clusters=10)
y_kmeans10 = kmeans10.fit_predict(df)
x = df.iloc[:, 1:].values

print(df.shape)
print(y_kmeans10)


#Ecrire le cluster
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