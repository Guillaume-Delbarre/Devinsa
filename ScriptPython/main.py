# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 19:27:27 2020

@author: pjzoe
"""
from MiseEnPage import miseEnPage
from kmeans import kmeansAlgo
from PCA import to2D
from ScriptPCA import PCA

def main(numberOfClusters=6, visualisation="TSNE"):
    miseEnPage()
    kmeansAlgo(numberOfClusters)
    if visualisation == "TSNE":
        to2D()
    elif visualisation=="PCA":
        PCA()
        
if __name__ == '__main__':
    main()
            
