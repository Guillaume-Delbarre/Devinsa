# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 19:27:27 2020

@author: pjzoe
"""
from MiseEnPage import miseEnPage
from kmeans import kmeansAlgo
from CHA import classHierarchique
from visualisation import to2D
from questionsCaracteristiques import printQuestionCarac

import time
import sys

def main():
    numberOfClusters=4
    nbQuestion=10
    if (len(sys.argv) == 3):
        numberOfClusters=int(sys.argv[1])
        nbQuestion=int(sys.argv[2])
    temps = time.time()
    miseEnPage()
    print("Temps mis en page : %s secondes ---" % (time.time() - temps))
    #kmeansAlgo(numberOfClusters)
    classHierarchique(numberOfClusters)
    print("Temps Classification hierarchique : %s secondes ---" % (time.time() - temps))
    printQuestionCarac(numberOfClusters,nbQuestion)
    print("Temps print question carac : %s secondes ---" % (time.time() - temps))
    to2D()
    print("Temps to 2 D : %s secondes ---" % (time.time() - temps))
        
if __name__ == '__main__':
    main()
            
