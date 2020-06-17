# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:52:42 2019
@author: Guillaume
"""
#import matplotlib.pyplot as plt
import pandas as pd
import sys

from sklearn.manifold import TSNE
#from sklearn import datasets
#from sklearn.decomposition import PCA
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from random import *


def to2D():
    #Prendre les titres des questions
    file_question = open("../Donnees/classif.csv","r",encoding='utf-8')
    first = file_question.readline()
    file_question.close()
    
    listTitres = first.split(';')
    listTitres[len(listTitres)-1] = listTitres[len(listTitres)-1].replace("\n","")
    del listTitres[0]
    del listTitres[len(listTitres)-1]
    
    
    #Charge le dataFrame avec toutes les infos du fichier
    df = pd.read_csv("../Donnees/classif.csv", sep = ';' , header = 0, encoding='utf-8')
    
    
    y = df.loc[:,'id'].values
    x = df.loc[:, listTitres].values
    
    cluster = df.loc[:,'Clusters'].values
    #med = df.loc[:,'Medoid'].values
    
    
    pca = TSNE(n_components=2)
    x_r = pca.fit_transform(x)
    
    file_zero = open("../Donnees/resVisualisation.csv","w",encoding='utf-8')
    file_zero.write("Axe_X,Axe_Y,id,Cluster\n")
    file_zero.close()
    
    file = open("../Donnees/resVisualisation.csv","a",encoding="utf-8")
    
    
    for i in range(len(x_r)) :
        x0 = str(x_r[i,0])
        x1 = str(x_r[i,1])
        
        file.write(x0 + "," + x1 + "," + str(y[i]) + "," + "Groupe " + str(cluster[i]) + "\n")
    
    file.close()

if __name__ == '__main__':
    to2D()

"""
Affiches le pourcentage d'importance des deux axes finaux
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))
yes = str(pca.explained_variance_ratio_).split()
file = open("variance.csv","w",encoding="utf-8")
for i in range(len(yes)) :
   file.write(yes[i] + "\n")
file.close()
#plot les points
plt.title('PCA')
plt.scatter(x_r[:,0],x_r[:,1])
plt.show()
"""