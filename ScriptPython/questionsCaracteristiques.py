# -*- coding: utf-8 -*-

import pandas as pd

medoids = None


def ecritQuestionCarac(df,agg,nbCluster,nbQuestion):
    file = open("../Donnees/infoClusters.csv","w")
    file.write("Cluster;Medoid;")
    for i in range(nbQuestion-1):
        file.write("Q"+str(i)+";")
    file.write("Q"+str(nbQuestion-1)+"\n")

    for i in range(nbCluster):
        agg_sorted = agg.sort_values(by=i, axis=1, ascending=False)
        file.write(str(i)+";"+medoids[i]+";")
        j=0
        for column in agg_sorted.columns:
            if j>=nbQuestion:
                break
            else: 
                file.write(column+";")
            j=j+1
        file.write("\n")

def getQCarac(nbCluster=6, nbQuestion=5):
    global medoids
    df = pd.read_csv("../Donnees/kmeans.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
    df.sort_values(by='Clusters', inplace=True)
    medoids = df.loc[df['Medoid']==1].index.values
    del df['Medoid']
    agg = df.groupby(['Clusters']).agg("mean")
    ecritQuestionCarac(df,agg,nbCluster,nbQuestion)
    
    

if __name__ == '__main__':
    getQCarac()
    