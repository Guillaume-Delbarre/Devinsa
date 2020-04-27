# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics import pairwise_distances

df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'utf-8')

def differences2Cluster(L1,L2):
    

def differences2Selection(L1,L2):

def differencesSelectionCluster(L1,L2):
    



if __name__ == '__main__':
    if (len(sys.argv) == 3):
        L1=int(sys.argv[1])
        L2=int(sys.argv[2])
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
        differences2Cluster([2],[1])