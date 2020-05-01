# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics import pairwise_distances
import re

df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')

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

def differences2Selection(L1,L2):
    global df
    countS1 = len(L1)
    countS2 = len(L2)
    S1 = pd.DataFrame(df.loc[L1, :], copy=True)
    S2 = pd.DataFrame(df.loc[L2, :], copy=True)
    del S1["Clusters"]
    del S2["Clusters"]
    S1 = S1/countS1
    S2 = S2/countS2
    res = np.subtract(S1,S2).abs()
    res.sort_values(by= [L1[0]], axis = 'columns', inplace=True, ascending = False )
    print(res.columns)

def differencesSelectionCluster(L1,L2):
    global df
    countS = len(L1)
    countC = len(df[df["Clusters"]==L2[0]])
    somme = pd.DataFrame(df.groupby(['Clusters'],as_index=False).sum())
    C = pd.DataFrame(somme[somme["Clusters"]==L2[0]], copy=True)
    del C["Clusters"]
    S = pd.DataFrame(df.loc[L1, :], copy=True)
    del S["Clusters"]
    print(S)
    C = C/countC
    S = S/countS
    res = np.subtract(S,C).abs()
    res.sort_values(by= [L1[0]], axis = 'columns', inplace=True, ascending = False )
    print(res.columns)



if __name__ == '__main__':
    if (len(sys.argv) == 3):
        L1=int(sys.argv[1])
        L2=int(sys.argv[2])
        regex = re.compile("Groupe (.)")
        r1 = regex.search(L1)
        r2 = regex.search(L2)
        if r1!=None:
            L1=[int(r1.group(1))]
        if r2!=None:
            L2=[int(r2.group(1))]
            
        if(isinstance(L1[0], int) and isinstance(L2[0], int)):
            differences2Cluster(L1,L2)
        elif(isinstance(L1[0], str) and isinstance(L2[0], str)):
            differences2Selection(L1,L2)
        elif(isinstance(L1[0], str) and isinstance(L2[0], int)):
            differencesSelectionCluster(L1,L2)
        elif(isinstance(L1[0], int) and isinstance(L2[0], str)):
            differencesSelectionCluster(L2,L1)
        else:
            raise ValueError("Erreur dans les type des paramètres")

    else:
        differencesSelectionCluster(["Batman", "Donald Trump"],[0])