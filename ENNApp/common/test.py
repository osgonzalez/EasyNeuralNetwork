import pandas as pd 
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import sys
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
# tensorflow
import tensorflow
# keras
import keras
from keras.models import Sequential
from keras.layers.core import Dense


print("....................................")
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
dataSetsPath = os.path.join(BASE_DIR, "ds.csv")
dataframe = pd.read_csv(dataSetsPath, header=0)

cols = dataframe.columns.tolist()

X = dataframe[cols[:-1]].to_numpy()
#X = np.reshape(X,(1000,5))
Y = dataframe[cols[-1:]].to_numpy()
'''
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
sc = StandardScaler()
Y = sc.fit_transform(Y)
'''

model = Sequential()
model.add(Dense(5, activation='relu', input_dim=5))
#model.add(Dense(5, activation='relu', input_shape=(1,)))
model.add(Dense(5, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='mean_squared_error', optimizer='sgd')


print("....................................")
print("....................................")
print(X)
print("....................................")
print("....................................")

#model.fit(Y, X, epochs=100)
model.fit(X, Y, epochs=100)