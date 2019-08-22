import pandas as pd 
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np


def getSamples(datasetPaht, numSamples=30):
    dataframe = pd.read_csv(datasetPaht, header=0)
    sample = dataframe.sample(n=numSamples) if dataframe.shape[0] >= numSamples else dataframe
    #sample = dataframe.sample(n=numMuestras).shape
    #dataframe.sample(n=numMuestras, random_state=1) Produce siempre los mismos resultados

    print("--------------------------------------")
    #print(dataframe.info(verbose=True))
    print("--------------------------------------")
    print("--------------------------------------")

    print("--------------------------------------")
    print("--------------------------------------")

    
    scalar = StandardScaler()
    scalar.fit(dataframe)
    print(scalar.get_params())
    scalarParams = scalar.get_params(deep=True)
    scalarParams2 = scalar.get_params(deep=False)
    means = scalar.mean_ 
    vars = scalar.var_


    toRet = {
        "sample": sample,
        "description": dataframe.describe(include="all").to_html(table_id="dataframeDescription", justify="left"),
        "tablehtml": sample.to_html(table_id="dataframeSample", justify="left", index =False),
        "profile": "profile.html",
        "corr":  dataframe.corr().to_html(table_id='correlations', justify="left"),
        "collNames": dataframe.columns.tolist()

    }
    return toRet

'''
DataFrame.count
Count number of non-NA/null observations.
DataFrame.max
Maximum of the values in the object.
DataFrame.min
Minimum of the values in the object.
DataFrame.mean
Mean of the values.
DataFrame.std
Standard deviation of the observations.
DataFrame.select_dtypes
Subset of a DataFrame including/excluding columns based on their dtype.
'''


def writeDataset(dataframe, datasetPath):
    dataframe.to_csv(path_or_buf=datasetPath,columns=dataframe.columns.tolist(), index=False)

def preprocessDataset(parameters, datasetDir):

    oldDatasetPath = os.path.join(datasetDir,parameters['datasetName']) 
    newdatasetPath = oldDatasetPath if parameters["OverwriteFile"] == "True" else os.path.join(datasetDir,parameters['newFileName'])
    
    dataframe = pd.read_csv(oldDatasetPath, header=0)

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

    # Select Target

    cols = dataframe.columns.tolist()
    if not cols[-1:][0] == parameters["targetColl"]:
        newIndex = []
        
        for col in cols:
            if not col == parameters["targetColl"]:
                newIndex.append(col)
        
        newIndex.append(parameters["targetColl"])
        print("....................,.,.,.,.,.,")
        print(cols)
        print(newIndex)
        dataframe = dataframe[newIndex]



    writeDataset(dataframe,newdatasetPath)

    toRet = {
        "test": "sample",
        "datasetName": parameters['datasetName'] if parameters["OverwriteFile"] == "True" else parameters['newFileName']
    }
    return toRet