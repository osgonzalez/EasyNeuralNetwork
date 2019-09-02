from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User as userModel
from django.contrib.auth.decorators import login_required
import os, time
import math
from ..common import preprocessing
from ..common import neural
import json





@login_required(login_url='/login/')
def listNeuralNetwork(request):
    downloadNeuralNetworkUrl = "/files/" + request.user.username + "/neuralNetwork/"
    deleteNeuralNetworkUrl = "/deleteNeuralNetwork/" + request.user.username + "/" 

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    neuralNetworkPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "neuralNetwork")

    context = {}

    if not os.path.exists(neuralNetworkPath):
        context.update({'secondaryMessageErr': "You haven't any Neural Network yet"})
    else:
        neuralNetworks = []
        for file in os.listdir(neuralNetworkPath):
            filepath = os.path.join(neuralNetworkPath, file)
            if os.path.isfile(filepath):
                #Get Code and Model
                codeUrl = ""
                infoUrl = ""
                fileBaseName = str(file).rstrip('.HDF5')
                modelPath = os.path.join(BASE_DIR, "userFiles", request.user.username, "model", "code", (fileBaseName + ".py"))
                infoPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info", (fileBaseName + ".info"))
                
                if(os.path.exists(modelPath)):
                    codeUrl = "/files/" + request.user.username + "/model/code/" + (fileBaseName + ".py")
                if(os.path.exists(infoPath)):
                    infoUrl = "/files/" + request.user.username + "/model/info/" + (fileBaseName + ".info")

                #Append Data
                neuralNetworks.append({
                    "name": file, 
                    "userOwner": request.user.username , 
                    "creationDate": time.ctime(os.path.getctime(filepath)), 
                    "size": convert_size(os.path.getsize(filepath)), 
                    "url": ( downloadNeuralNetworkUrl + file), 
                    "deleteUrl": deleteNeuralNetworkUrl + file + "/",
                    "infoUrl": infoUrl,
                    "codeUrl": codeUrl
                    })
        
        if request.user.is_superuser:
            baseNeuralNetworkPath = os.path.join(BASE_DIR, "userFiles")
            for userDir in os.listdir(baseNeuralNetworkPath):
                if userDir != request.user.username and os.path.exists(os.path.join(baseNeuralNetworkPath, userDir, "neuralNetwork")):
                    deleteNeuralNetworkUrl = "/deleteNeuralNetwork/" + userDir + "/"
                    userNetworkPath = os.path.join(baseNeuralNetworkPath, userDir, "neuralNetwork") 
                    downloadNeuralNetworkUrl = "/files/" + userDir + "/neuralNetwork/"
                    for file in os.listdir(userNetworkPath):
                        filepath = os.path.join(userNetworkPath, file)
                        if os.path.isfile(filepath):
                            #Get Code and Model
                            codeUrl = ""
                            infoUrl = ""
                            fileBaseName = str(file).rstrip('.HDF5')
                            modelPath = os.path.join(BASE_DIR, "userFiles", userDir, "model", "code", (fileBaseName + ".py"))
                            infoPath = os.path.join(BASE_DIR, "userFiles", userDir , "model", "info", (fileBaseName + ".info"))
                            
                            if(os.path.exists(modelPath)):
                                codeUrl = "/files/" + userDir + "/model/code/" + (fileBaseName + ".py")
                            if(os.path.exists(infoPath)):
                                infoUrl = "/files/" + userDir + "/model/info/" + (fileBaseName + ".info")

                            #Append Data
                            neuralNetworks.append({
                                "name": file, 
                                "userOwner": userDir , 
                                "creationDate": time.ctime(os.path.getctime(filepath)), 
                                "size": convert_size(os.path.getsize(filepath)), 
                                "url": ( downloadNeuralNetworkUrl + file), 
                                "deleteUrl": deleteNeuralNetworkUrl + file + "/",
                                "infoUrl": infoUrl,
                                "codeUrl": codeUrl
                                })
        
             
        context.update({'neuralNetworks': neuralNetworks})
    
    loadContextMessages(request,context)
    
    return render(request, 'ENNApp/listNeuralNetworks.html', context)

@login_required(login_url='/login/')
def deleteNeuralNetwork(request, userName, fileName):
    try:
        if request.user.is_superuser or request.user.username == userName:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            neuralNetworkPath = os.path.join(BASE_DIR, "userFiles", userName , "neuralNetwork", fileName)
            fileBaseName = str(fileName).rstrip('.HDF5')
            modelPath = os.path.join(BASE_DIR, "userFiles", userName, "model", "code", (fileBaseName + ".py"))
            infoPath = os.path.join(BASE_DIR, "userFiles", userName , "model", "info", (fileBaseName + ".info"))
            
            os.remove(neuralNetworkPath)
            if(os.path.exists(modelPath)):
                os.remove(modelPath)
            if(os.path.exists(infoPath)):
                os.remove(infoPath)

            request.session['messageOk'] = "Neural Network was deleted successfully"
        else:
            request.session['messageErr'] = "You don't have enough permissions to do this action"
    except:
        request.session['messageErr'] = "An error occurred deleting the file"
    return redirect('listNeuralNetwork')

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def loadContextMessages(request,context):
    if 'messageErr' in request.session:
        context.update({"messageErr": request.session['messageErr']})
        del request.session['messageErr']
    if 'messageOk' in request.session:
        context.update({"messageOk": request.session['messageOk']})
        del request.session['messageOk']


@login_required(login_url='/login/')
def createModel(request, fileName, oldContext={}):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", fileName)

    context = {}
    context.update(oldContext)

    if not os.path.exists(dataSetsPath):
        context.update({'secondaryMessageErr': "this file does not exist"})
    else:
       
        try:
            toRet = preprocessing.getColsNames(dataSetsPath)
            context.update(toRet)

        except BaseException as e:
            context.update({"messageErr": "An error occurred reading the file (" + str(e) +")"})
    
    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    return render(request, 'ENNApp/createModel.html', context)



@login_required(login_url='/login/')
def executeModel(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", request.POST["datasetName"])
    userFolderPath = os.path.join(BASE_DIR, "userFiles", request.user.username)
    context = {}

    if not os.path.exists(dataSetsPath):
        context.update({'messageErr': "this dataset does not exist"})
    else:
        try:       
            models = json.loads(request.POST["data"])
            rowData = json.loads(request.POST["rowData"])
            toRet = neural.executeModel(models, rowData, dataSetsPath, userFolderPath)
            context.update(toRet)
            


        except BaseException as e:
            context.update({"messageErr": "An error occurred (" + str(e) +")"})

    if 'messageErr' not in context:
        request.session['messageOk'] = "All models have been executed successfully"
    else:
        request.session['messageErr'] = context["messageErr"]

    return HttpResponse("Ok")


@login_required(login_url='/login/')
def detailNeuralNetwork(request, fileName):
    fileBaseName = str(fileName).rstrip('.HDF5')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    infoPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "model", "info", (fileBaseName + ".info"))
                
    context = {}

    if not os.path.exists(infoPath):
        context.update({'secondaryMessageErr': "this file does not exist"})
    else:
       
        try:
            toRet = neural.readInfoFile(infoPath)
            print(str(toRet))
            data = json.loads(toRet)
            print(type(data))
            context.update(data)

        except BaseException as e:
            context.update({"messageErr": "An error occurred reading the file (" + str(e) +")"})
    
    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    return render(request, 'ENNApp/neuralNetworkDetail.html', context)