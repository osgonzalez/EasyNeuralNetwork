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
from .untils import readDataset, writeDataset, writeFile, createDirIfNotExist

#from sklearn.model_selection import StratifiedKFold
#kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=5)


def executeModel(models, rowData, datasetPath, userFolderPath):

    neuralNetworkFolderPath = os.path.join(userFolderPath, "neuralNetwork")
    modelFolderPath = os.path.join(userFolderPath, "model", "code")
    infoFolderPath = os.path.join(userFolderPath, "model", "info")

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
            batchSize = int(models[modelName]["batchSize"])
            model.fit(X_train, y_train, epochs=epochs, batch_size=batchSize)
            
            #Model summary
            print(model.summary())

            # evaluate the model
            lossVal = str(model.evaluate(X_test, y_test, verbose=0)*100) + "%"
            models[modelName]["lossVal"] = lossVal
            print(lossVal)
            
            #Create model auto-generated code
            autoGeneratedCode = generateCode(models[modelName])
            codeModelName = str(modelName).rstrip('.csv') + ".py"
            writeFile(autoGeneratedCode, modelFolderPath, codeModelName)
            
            #Create NeuralNetwork File
            neuralNetworkName = str(modelName).rstrip('.csv') + ".HDF5"
            createDirIfNotExist(neuralNetworkFolderPath)
            neuralNetworkPath = os.path.join(neuralNetworkFolderPath, neuralNetworkName)
            model.save(neuralNetworkPath)

            #Create info File
            infoFileName = str(modelName).rstrip('.csv') + ".info"
            writeFile(str(models[modelName]), infoFolderPath, infoFileName)
            

        except BaseException as e:
            print("Error -> " + str(e))
            if toRet["messageErr"] is not None:
                toRet.update({"messageErr": "An error occurred in Model " + modelName})
            else:
                toRet.update({"messageErr": toRet["messageErr"] + ", " + modelName})
    
 

def generateCode(model):
    code = ""
    code += '#------------------------------------------------------------------------------\n'
    code += '# <auto-generated>\n'
    code += '#     This code was generated by Easy Neural Network\n'
    code += '#     Runtime Version:1.0\n'
    code += '#\n'
    code += '#     Changes to this file may cause incorrect behavior and will be lost if\n'
    code += '#     the code is regenerated.\n'
    code += '# </auto-generated>\n'
    code += '#------------------------------------------------------------------------------\n'
    code += '\n'
    code += '\n'
    code += '# pandas\n'
    code += 'import pandas as pd \n'
    code += '# numpy\n'
    code += 'import numpy as np\n'
    code += '# sklearn\n'
    code += 'from sklearn.preprocessing import StandardScaler, MinMaxScaler\n'
    code += 'from sklearn.model_selection import train_test_split\n'
    code += '# tensorflow\n'
    code += 'import tensorflow\n'
    code += '# keras\n'
    code += 'import keras\n'
    code += 'from keras.models import Sequential\n'
    code += 'from keras.layers.core import Dense\n'
    code += '\n'
    code += '\n'

    code += 'def generateNeuralNetwork(trainData,trainTarget):\n'
    code += '    #Clear Sesion\n'
    code += '    keras.backend.clear_session()\n'
    code += '\n'
    code += '    #Create the secuential model\n'
    code += '    model = Sequential()\n'
    code += '\n'
    code += '    #Imput Layer\n'
    code += '    dimNumber = int(' + str(model["firstDimNumber"]) + ')\n'
    code += '    activation = "' + str(model["firstActivation"]) + '" \n'
    code += '    model.add(Dense(dimNumber, activation=activation,input_dim=dimNumber))\n'
    for hidenLayer in model["hidenLayers"]:
        code += '    \n'
        code += '    #Hidden Layer ' + hidenLayer + '\n'
        code += '    dimNumber = int('+ str(model["hidenLayers"][hidenLayer]["dimNumber"]) +')\n'
        code += '    activation = str("'+ str(model["hidenLayers"][hidenLayer]["activation"])+'")\n'
        code += '    model.add(Dense(dimNumber, activation=activation))\n'
    code += '    \n'
    code += '    #Output Layer\n'
    code += '    dimNumber = int('+ str(model["lastDimNumber"]) + ')\n'
    code += '    activation = str("'+ str(model["lastActivation"])+ '")\n'
    code += '    model.add(Dense(dimNumber, activation=activation))\n'
    code += '\n'
    code += '    #Compile the model\n'
    code += '    lossFuntion = str("'+ str(model["lossFuntion"])+ '")\n'
    code += '    optimicer = str("'+ str(model["optimicer"])+ '")\n'
    code += '    model.compile(loss=lossFuntion, optimizer=optimicer)\n'
    code += '\n'
    code += '\n'
    code += '    #Fit the model whith the train data (and indicate the numer of iterations for the data)\n'
    code += '    epochs = int('+ str(model["epochs"]) + ')\n'
    code += '    batchSize = int('+ str(model["batchSize"]) + ')\n'
    code += '    model.fit(trainData, trainTarget, epochs=epochs, batch_size=batchSize)\n'
    code += '    \n'
    code += '    #Model summary\n'
    code += '    print(model.summary())\n'

    return code