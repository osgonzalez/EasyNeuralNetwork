import pandas as pd 
import pandas_profiling


def getSamples(datasetPaht, numSamples=30):
    dataframe = pd.read_csv(datasetPaht, header=0)
    sample = dataframe.sample(n=numSamples) if dataframe.shape[1] >= numSamples else dataframe
    #sample = dataframe.sample(n=numMuestras).shape
    #dataframe.sample(n=numMuestras, random_state=1) Produce siempre los mismos resultados

    print("--------------------------------------")
    #print(dataframe.info(verbose=True))
    print("--------------------------------------")
    print("--------------------------------------")
    #profile = sample.profile_report(minify_html=False,missing_diagrams={"bar":False,"matrix":False,"heatmap":False, "dendrogram": False})
    #print(type(dataframe.corr()))
    print("--------------------------------------")
    print("--------------------------------------")


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
    dataframe.to_csv(path_or_buf=datasetPath)
