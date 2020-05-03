# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics import pairwise_distances
import re

df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')
"""
def differences2Cluster(L1,L2):
    global df
    C1 = len(df[df["Clusters"]==L1[0]])
    C2 = len(df[df["Clusters"]==L2[0]])
    somme = pd.DataFrame(df.groupby(['Clusters'],as_index=False).sum())
    S1 = pd.DataFrame(somme[somme["Clusters"]==L1[0]], copy=True)
    S2 = pd.DataFrame(somme[somme["Clusters"]==L2[0]], copy=True)
    del S1["Clusters"]
    del S2["Clusters"]
    S1 = S1/C1
    S2 = S2/C2
    res = np.subtract(S1,S2).abs()
    res.sort_values(by= [L1[0]], axis = 'columns', inplace=True, ascending = False )
    print(res.columns)
"""
def differences2Selection(L1,L2):
    global df
    countS1 = len(L1)
    countS2 = len(L2)
    S1 = pd.DataFrame(pd.DataFrame(df.loc[L1, :], copy=True).sum())
    S2 = pd.DataFrame(pd.DataFrame(df.loc[L2, :],copy=True).sum())
    S1=S1.T
    S2=S2.T
    del S1["Clusters"]
    del S2["Clusters"]
    S1 = S1/countS1
    S2 = S2/countS2
    res = np.subtract(S1,S2)
    res= res.T
    res = res.reindex(res[0].abs().sort_values(ascending = False).index)
    print(res)
    res = res.iloc[:20,:]
    res = res.reset_index()
    res.columns=['Question','Différences']
    res.to_csv("../Donnees/differences.csv", mode='w', index=True)


def differencesSelectionCluster(L1,L2):
    global df
    countS = len(L1)
    countC = len(df[df["Clusters"]==L2[0]])
    somme = pd.DataFrame(df.groupby(['Clusters'],as_index=False).sum())
    C = pd.DataFrame(somme[somme["Clusters"]==L2[0]], copy=True)
    del C["Clusters"]
    S = pd.DataFrame(pd.DataFrame(df.loc[L1, :] ,copy=True).sum())
    S=S.T
    del S["Clusters"]
    C = C/countC
    S = S/countS
    res = np.subtract(S,C)
    res= res.T
    res = res.reindex(res[0].abs().sort_values(ascending = False).index)
    res = res.iloc[:20,:]
    res = res.reset_index()
    res.columns=['Question','Différences']
    res.to_csv("../Donnees/differences.csv", mode='w', index=False)



def differences(L1,L2):

    L1= str(L1).replace("[","").replace("]","")
    L1 = L1.split(",")

    regex = re.compile("Groupe (.)")
    groupe = regex.search(L2)
    # 2e parametre est un cluster
    if groupe!=None:
        L2=[int(groupe.group(1))]  
    else:
        L2= str(L2).replace("[","").replace("]","")
        L2 = L2.split(",")
    if(isinstance(L1[0], str) and isinstance(L2[0], str)):
        differences2Selection(L1,L2)
    elif(isinstance(L1[0], str) and isinstance(L2[0], int)):
        differencesSelectionCluster(L1,L2)
    else:
        raise ValueError("Erreur dans les paramètres")

if __name__ == '__main__':

    if (len(sys.argv) == 3):
        L1=sys.argv[1]
        L2=sys.argv[2]
        
        differences(L1,L2)
    

        