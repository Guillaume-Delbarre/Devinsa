# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Mon Jan 27 12:17:33 2020
@author: pjzoe
"""
import pandas as pd
from keras.layers import Dense, Input
from keras.models import Model


def autoencoder2D():
    
    df = pd.read_csv("../Donnees/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
    
   
    entree = Input(shape=(902,))
    inter = Dense(units=100, activation='relu')(entree)
    enc = Dense(units=2, activation ='linear')(inter)
    inter = Dense(units=100, activation='relu')(enc)
    sortie = Dense(units=902, activation ='linear')(inter)
    
    autoEnc = Model(inputs=entree,outputs=sortie)
    autoEnc.compile(loss='mse',optimizer='adam',metrics=['mae'])

    enc = Model(inputs=entree,outputs=enc)
    enc.compile(loss='mse',optimizer='adam',metrics=['mae'])
    autoEnc.summary()
    autoEnc.fit(df,df,epochs=20,batch_size=4)
    return enc.predict(df)
    

