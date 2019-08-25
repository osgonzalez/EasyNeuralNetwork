import pandas as pd 
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import sys


def getSamples(datasetPaht, numSamples=30):
    dataframe = readDataset(datasetPaht)
    sample = dataframe.sample(n=numSamples) if dataframe.shape[0] >= numSamples else dataframe
    #sample = dataframe.sample(n=numMuestras).shape
    #dataframe.sample(n=numMuestras, random_state=1) Produce siempre los mismos resultados


    #Get Cateforicos
    cols = dataframe.columns

    numericCols = dataframe._get_numeric_data().columns

    categoricCols = list(set(cols) - set(numericCols))
    #End Get Categoricos

    toRet = {
        "sample": sample,
        "description": dataframe.describe(include="all").to_html(table_id="dataframeDescription", justify="left"),
        "tablehtml": sample.to_html(table_id="dataframeSample", justify="left", index =False),
        "profile": "profile.html",
        "corr":  dataframe.corr().to_html(table_id='correlations', justify="left"),
        "collNames": dataframe.columns.tolist(),
        "categoricCols": categoricCols

    }
    return toRet

def readDataset(datasetPath):
    return pd.read_csv(datasetPath, header=0)

def writeDataset(dataframe, datasetPath):
    dataframe.to_csv(path_or_buf=datasetPath,columns=dataframe.columns.tolist(), index=False)

def preprocessDataset(parameters, datasetDir):

    oldDatasetPath = os.path.join(datasetDir,parameters['datasetName']) 
    newdatasetPath = oldDatasetPath if parameters["OverwriteFile"] == "True" else os.path.join(datasetDir,parameters['newFileName'])
    
    dataframe = readDataset(oldDatasetPath)

    #Delete Cols
    colsToDeleteList = parameters.getlist('deleteCols[]')  
    if colsToDeleteList:
        actualCols = dataframe.columns.tolist()
        finalCols = list(set(actualCols) - set(colsToDeleteList))
        dataframe = dataframe[finalCols]

    #One Hot Encoding
   
    #Encoding All categorical Colums
    dataframe = pd.get_dummies(dataframe)
    #Encoding Selected Colums
    oneHotList = parameters.getlist('oneHotList[]')
    if oneHotList: #is not empty
        dataframe = pd.get_dummies(dataframe,columns=oneHotList ,prefix=oneHotList)


    #Check NaN

    if parameters["valuesNull"] == "colMean":
        dataframe = dataframe.fillna(dataframe.mean())
    
    if parameters["valuesNull"] == "colMedian":
        dataframe = dataframe.fillna(dataframe.median())

    if parameters["valuesNull"] == "ColMode":
        dataframe = dataframe.fillna(dataframe.mode().ix[0])

    if parameters["valuesNull"] == "custom":
        customNumber = parameters["customNumber"] if parameters["customNumber"].lstrip('-+').isdigit() else 0
        dataframe = dataframe.fillna(customNumber)

    #Normalize

    if parameters["normalize"] == "Standardize":
        scaler = StandardScaler()
        scaledNumpyArr = scaler.fit_transform(dataframe)
        dataframe = pd.DataFrame(scaledNumpyArr, columns=dataframe.columns)
    
    if parameters["normalize"] == "Scale":
        scaler = MinMaxScaler()
        scaledNumpyArr = scaler.fit_transform(dataframe)
        dataframe = pd.DataFrame(scaledNumpyArr, columns=dataframe.columns)



    writeDataset(dataframe,newdatasetPath)

    toRet = {
        "test": "sample",
        "datasetName": parameters['datasetName'] if parameters["OverwriteFile"] == "True" else parameters['newFileName']
    }
    return toRet




def principalComponentAnalysis(parameters, datasetPath):
    
    dataframe = readDataset(datasetPath)

    # Select Target

    '''
    cols = dataframe.columns.tolist()
    if not cols[-1:][0] == parameters["targetColl"]:
        newIndex = []
        
        for col in cols:
            if not col == parameters["targetColl"]:
                newIndex.append(col)
        
        newIndex.append(parameters["targetColl"])
        dataframe = dataframe[newIndex]
    '''
    targetCols = parameters.getlist('targetColls[]')
    cols = dataframe.columns.tolist()
    X = dataframe[cols]
    Y = dataframe[targetCols]

    npCovarianceMatrix = np.cov(X.T)

    eig_vals, eig_vecs = np.linalg.eig(npCovarianceMatrix)

    
    #  Hacemos una lista de parejas (autovector, autovalor) 
    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

    # Ordenamos estas parejas den orden descendiente con la función sort
    eig_pairs.sort(key=lambda x: x[0], reverse=True)

    # Visualizamos la lista de autovalores en orden desdenciente
    print('Autovalores en orden descendiente:')
    for i in eig_pairs:
        print(i[0])


    writeDataset(dataframe,datasetPath)

    toRet = {
        "test": "sample"
    }
    return toRet






'''
#cols = dataframe.columns.tolist()
#newDataframeCols = pd.DataFrame()
for oneHotCol in oneHotList:
    try:
        #newDataframeCols = pd.get_dummies(dataframe,prefix=oneHotCol) + newDataframeCols
        dataframe = pd.get_dummies(dataframe,prefix=oneHotCol)
    except ValueError as e:
        print("\n--------- Error ---------\n",e,"\n--------- End ---------\n")
        #pass
#cols = list(set(cols) - set(oneHotList))
#dataframe = dataframe[cols] + newDataframeCols
#dataframe = dataframe[cols]
'''