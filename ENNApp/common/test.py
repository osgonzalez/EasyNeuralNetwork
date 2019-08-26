import pandas as pd 
import os

print("....................................")
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
dataSetsPath = os.path.join(BASE_DIR, "ds.csv")
dataframe = pd.read_csv(dataSetsPath, header=0)
print(dataframe)

'''
'''
print("....................................")
print("....................................")
print("....................................")
print("....................................")

'''
cols = dataframe.columns.tolist()
print(cols)

cols = cols[-1:] + cols[:-1]
print(cols)
print("------------------------------------")
dataframe = dataframe[cols]
print(dataframe)

dataframe.to_csv(path_or_buf=os.path.join(BASE_DIR, "ds2.csv"))
'''

dataframe = dataframe.fillna(dataframe.mean())
cols = dataframe.columns.tolist()
X = dataframe[cols[:-1]]
Y = dataframe[cols[-1:]]

from sklearn.preprocessing import StandardScaler
X = StandardScaler().fit_transform(X)

#

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(X)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, Y], axis = 1)

print(finalDf)
print(pca.explained_variance_ratio_)
print("Loss")
print(pca.explained_variance_ratio_.sum())


print("--------------------.----------------.------------------------.--------------------.")


pca = PCA(.95)
principalComponents = pca.fit_transform(X)
colNames = []
for i in range(pca.n_components_ ):
    colNames.append("Component "+ str(i))
principalDf = pd.DataFrame(data = principalComponents, columns = colNames)
finalDf = pd.concat([principalDf, Y], axis = 1)

print(finalDf)
print(pca.n_components_)