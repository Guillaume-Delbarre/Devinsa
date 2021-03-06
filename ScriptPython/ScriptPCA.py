# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:52:42 2019

@author: Guillaume
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
from sklearn.decomposition import KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def PCA():
    #Prendre les titres des questions
    file_question = open("../Donnees/kmeans.csv","r")
    first = file_question.readline()
    file_question.close()
    listTitres = first.split(';')
    listTitres[len(listTitres)-1] = listTitres[len(listTitres)-1].replace("\n","")
    del listTitres[0]
    
    #Charge le dataFrame avec toutes les infos du fichier
    df = pd.read_csv("../Donnees/kmeans.csv", sep = ';' , header = 0, encoding='latin-1')
    df = df.fillna(0)
    
    y = df.loc[:,'Noms'].values
    x = df.loc[:, listTitres].values
    
    cluster = df.loc[:,'Clusters '].values
    
    pca = KernelPCA(n_components=2, kernel="rbf")
    x_r = pca.fit_transform(x)
    
    file_zero = open("../Donnees/resPCA.csv","w")
    file_zero.write("Axe_X,Axe_Y,Name,Cluster\n")
    file_zero.close()
    
    file = open("../Donnees/resPCA.csv","a",encoding="utf-8")
    
    for i in range(len(x_r)) :
        x0 = str(x_r[i,0])
        x1 = str(x_r[i,1])
        print(x0)
        file.write(x0 + "," + x1 + "," + str(y[i]) + "," + "Groupe " + str(cluster[i]) + "\n")
    
    file.close()

if __name__ == '__main__':
    PCA()


"""
#plot les points
plt.title('PCA')
plt.scatter(x_r[:,0],x_r[:,1])
plt.show()
"""

