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




def principalComponentAnalysis(parameters, datasetDir):
    
    datasetPath = os.path.join(datasetDir,parameters['datasetName']) 

    dataframe = readDataset(datasetPath)

    # Select Target

    targetCols = parameters.getlist('targetColls[]')
    cols = dataframe.columns.tolist()
    dataCols = list(set(cols) - set(targetCols))

    X = StandardScaler().fit_transform(dataframe[dataCols])
    Y = dataframe[targetCols]

    if parameters["pcaAcuracy"] == "pcaAcuracy" :
        pcaAcuracyNumber = float(parameters["pcaAcuracyNumber"])/100
        pca = PCA(n_components=pcaAcuracyNumber)
    else:
        pcaDimNumber = int(parameters["pcaDimNumber"])
        pca = PCA(n_components=pcaDimNumber )

    principalComponents = pca.fit_transform(X)
    colNames = []
    for i in range(pca.n_components_ ):
        colNames.append("Component_"+ str(i))
    principalDf = pd.DataFrame(data = principalComponents, columns = colNames)
    
    dataframe = pd.concat([principalDf, Y], axis = 1)


    writeDataset(dataframe,datasetPath)

    toRet = {
        "test": "sample",
        "datasetName": parameters['datasetName'],
        "variance_ratio": ((pca.explained_variance_ratio_.sum())*100)
    }
    return toRet



def getColsNames(datasetPaht):
    dataframe = readDataset(datasetPaht)

    toRet = {
        "collNames": dataframe.columns.tolist()
    }
    return toRet

def executeModel(models, rowData, datasetPath):

    toRet = {}
    dataframe = readDataset(datasetPath)

    X = dataframe[rowData["dataNames"]].values
    Y = dataframe[rowData["targetsNames"]].values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

    
    for modelName in models:
        try:
            
            #Clear Sesion
            keras.backend.clear_session()

            #Create the secuential model
            model = Sequential()

            #Imput Layer
            dimNumber = int(models[modelName]["firstDimNumber"])
            activation = str(models[modelName]["firstActivation"])
            model.add(Dense(dimNumber, activation=activation,input_dim=dimNumber))
            
            #Hidden Layers
            for hidenLayer in models[modelName]["hidenLayers"]:
                dimNumber = int(models[modelName]["hidenLayers"][hidenLayer]["dimNumber"])
                activation = str(models[modelName]["hidenLayers"][hidenLayer]["activation"])
                model.add(Dense(dimNumber, activation=activation))
            
            #Output Layer
            dimNumber = int(models[modelName]["lastDimNumber"])
            activation = str(models[modelName]["lastActivation"])
            model.add(Dense(dimNumber, activation=activation))

            #Compile the model
            lossFuntion = str(models[modelName]["lossFuntion"])
            optimicer = str(models[modelName]["optimicer"])
            model.compile(loss=lossFuntion, optimizer=optimicer)


            #Fit the model whith the train data (and indicate the numer of iterations for the data)
            epochs = int(models[modelName]["epochs"])
            model.fit(X_train, y_train, epochs=epochs)
            
            #Model summary
            print(model.summary())




        except BaseException as e:
            print("Error -> " + str(e))
            if toRet["messageErr"] is not None:
                toRet.update({"messageErr": "An error occurred in Model " + modelName})
            else:
                toRet.update({"messageErr": toRet["messageErr"] + ", " + modelName})
    
    '''
    for coche in data:
    print(coche)
    print(data[coche]["marca"])
    print(data[coche]["modelo"])
    for tono in data[coche]["color"]:
        print(data[coche]["color"][tono])
    '''
