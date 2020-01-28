# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Mon Jan 27 12:17:33 2020

@author: pjzoe
"""
import pandas as pd
from keras.layers import Dense, Activation, Input
from keras.models import Model
from keras.optimizers import SGD
import numpy as np
import tensorflow as tf



#def modelePourVisualisation():
 #   entree = Input(shape=(902,))
  #  inter = Dense(units=100, activation='relu')(entree)
   # enc = Dense(units=2, activation ='linear')(inter)
    #inter = Dense(units=100, activation='relu')(enc)
    #sortie = Dense(units=902, activation ='linear')(inter)
    #model = Model(inputs=entree,outputs=sortie)
    #model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
    #return model


def main():
    df = pd.read_csv("C:/Users/pjzoe/Documents/3INFO/Etudes pratiques/GitHub/Données/Personnages.csv", sep = ";", header=0, index_col=0, encoding = 'latin1')
    df = df.to_numpy()
    print(df.shape)
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
    x_train = df
    print('x_train.shape=',x_train.shape)
    #x_train=x_train.reshape(1430,902)
    autoEnc.fit(x_train,x_train,epochs=20,batch_size=4)
    res = enc.predict(x_train)
if __name__ == "__main__":
	main()
