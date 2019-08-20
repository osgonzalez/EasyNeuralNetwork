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

cols = dataframe.columns.tolist()
print(cols)

cols = cols[-1:] + cols[:-1]
print(cols)
print("------------------------------------")
dataframe = dataframe[cols]
print(dataframe)

dataframe.to_csv(path_or_buf=os.path.join(BASE_DIR, "ds2.csv"))