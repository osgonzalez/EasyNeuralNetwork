import pandas as pd
import os

def readDataset(datasetPath):
    return pd.read_csv(datasetPath, header=0)


def writeDataset(dataframe, datasetPath):
    dataframe.to_csv(path_or_buf=datasetPath,columns=dataframe.columns.tolist(), index=False)


def writeFile(source,dir, filename):
    createDirIfNotExist(dir)
    filePath = os.path.join(dir, filename)

    f = open(filePath,"w+")
    f.write(source)
    f.close()

def createDirIfNotExist(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)