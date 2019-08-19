import pandas as pd 

def getSamples(numSamples,datasetPaht):
    try:
        dataframe = pd.read_csv(datasetPaht, header=0)
        sample = dataframe.sample(n=numSamples)
        #sample = dataframe.sample(n=numMuestras).shape
        #dataframe.sample(n=numMuestras, random_state=1) Produce siempre los mismos resultados
        print(dataframe)
        print("------------")
        print(sample)
        print("Done")
    except:
        print("Err!")

    print("End")

