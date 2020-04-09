# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 19:27:27 2020

@author: pjzoe
"""
from MiseEnPage import miseEnPage
from kmeans import kmeansAlgo
from CHA import classHierarchique
from PCA import to2D
from ScriptPCA import PCA
from questionsCaracteristiques import printQuestionCarac

def main(numberOfClusters=5, nbQuestion=10):
    miseEnPage()
    #kmeansAlgo(numberOfClusters)
    classHierarchique(numberOfClusters)
    printQuestionCarac(numberOfClusters,nbQuestion)
    to2D()
        
if __name__ == '__main__':
    main()
            
