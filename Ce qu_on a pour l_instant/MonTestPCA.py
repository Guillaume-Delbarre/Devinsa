# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:52:42 2019

@author: Guillaume
"""

import matplotlib.pyplot as plt

import pandas as pd

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis



#Prendre les titres des questions
file_question = open("test_des_res.csv","r")
first = file_question.readline()
file_question.close()
listTitres = first.split(';')
listTitres[len(listTitres)-1] = listTitres[len(listTitres)-1].replace("\n","")
del listTitres[0]
print(listTitres)


#Charge le dataFrame avec toutes les infos du fichier
df = pd.read_csv("test_des_res.csv", sep = ';' , header = 0, encoding='latin-1')

print(df)

y = df.loc[:,['Noms']].values

x = df.loc[:, listTitres].values

print(y)
print(x)

pca = PCA(n_components=2)
x_r = pca.fit(x).transform(x)


#lda = LinearDiscriminantAnalysis(n_components=2)
#x_r2 = lda.fit(x, y).transform(x)

print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))

plt.title('La meilleure PCA de tous les temps')
plt.scatter(x_r[:,0],x_r[:,1])





















