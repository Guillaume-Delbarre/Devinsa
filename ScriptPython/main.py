# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 19:27:27 2020

@author: pjzoe
"""
from MiseEnPage import miseEnPage
from kmeans import kmeansAlgo
from PCA import to2D
from ScriptPCA import PCA
from questionsCaracteristiques import getQCarac

def main(numberOfClusters=6):
    miseEnPage()
    kmeansAlgo(numberOfClusters)
    getQCarac(numberOfClusters)
    to2D()
        
if __name__ == '__main__':
    main()
            
