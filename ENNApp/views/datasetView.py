from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User as userModel
from django.contrib.auth.decorators import login_required
import os, time
import math
from ..common import preprocessing
from datetime import datetime


@login_required(login_url='/login/')
def uploadView(request):
    return render(request, 'ENNApp/upload.html')

@login_required(login_url='/login/')
def addDataset(request):
    if request.method == "POST" and request.FILES['dataSet']:
        dataSetFile = request.FILES["dataSet"]
        fileSystem = FileSystemStorage()
        userName = request.user.username
        filename = fileSystem.save( userName + "/datasets/" + dataSetFile.name, dataSetFile)
    return redirect('listDatasets')

@login_required(login_url='/login/')
def listDatasets(request):
    downloadDataSetUrl = "/files/" + request.user.username + "/datasets/"
    deleteDataSetUrl = "/deleteDataset/" + request.user.username + "/" 

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")

    context = {}

    if not os.path.exists(dataSetsPath):
        context.update({'secondaryMessageWarning': "You haven't any dataset yet"})
    else:
        datasets = []
        for file in os.listdir(dataSetsPath):
            filepath = os.path.join(dataSetsPath, file)
            if os.path.isfile(filepath):
                datasets.append({
                    "name": file, 
                    "userOwner": request.user.username , 
                    "creationDate": time.ctime(os.path.getctime(filepath)), 
                    #"creationDate": datetime.fromtimestamp(os.path.getctime(filepath)), 
                    "size": convert_size(os.path.getsize(filepath)), 
                    "url": ( downloadDataSetUrl + file), 
                    "deleteUrl": (deleteDataSetUrl + file + "/")})
        
        if request.user.is_superuser:
            baseDatasetPath = os.path.join(BASE_DIR, "userFiles")
            for userDir in os.listdir(baseDatasetPath):
                if userDir != request.user.username:
                    deleteDataSetUrl = "/deleteDataset/" + userDir + "/"
                    userDatasetPath = os.path.join(baseDatasetPath, userDir, "datasets") 
                    downloadDataSetUrl = "/files/" + userDir + "/datasets/"
                    for file in os.listdir(userDatasetPath):
                        filepath = os.path.join(userDatasetPath, file)
                        if os.path.isfile(filepath):
                            datasets.append({
                                "name": file, 
                                "userOwner": userDir , 
                                "creationDate": time.ctime(os.path.getctime(filepath)), 
                                "size": convert_size(os.path.getsize(filepath)), 
                                "url": ( downloadDataSetUrl + file), 
                                "deleteUrl": (deleteDataSetUrl + file + "/")})
        
             
        context.update({'datasets': datasets})
    
    loadContextMessages(request,context)
    
    return render(request, 'ENNApp/listDataset.html', context)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])



@login_required(login_url='/login/')
def deleteDataset(request, userName, fileName):
    try:
        if request.user.is_superuser or request.user.username == userName:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dataSetsPath = os.path.join(BASE_DIR, "userFiles", userName , "datasets", fileName)
            os.remove(dataSetsPath)
            request.session['messageOk'] = "Dataset was deleted successfully"
        else:
            request.session['messageErr'] = "You don't have enough permissions to do this action"
    except:
        request.session['messageErr'] = "An error occurred deleting the file"
    return redirect('listDatasets')



@login_required(login_url='/login/')
def showDatasetSample(request, fileName, oldContext={}):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets", fileName)

    context = {}
    context.update(oldContext)

    if not os.path.exists(dataSetsPath):
        context.update({'secondaryMessageErr': "this file does not exist"})
    else:
       
        try:
            toRet = preprocessing.getSamples(dataSetsPath)
            context.update(toRet)

        except BaseException as e:
            context.update({"messageErr": "An error occurred reading the file (" + str(e) +")"})
    
    loadContextMessages(request,context)
    context.update({"datasetName": fileName})
    return render(request, 'ENNApp/showDataset.html', context)


def loadContextMessages(request,context):
    if 'messageErr' in request.session:
        context.update({"messageErr": request.session['messageErr']})
        del request.session['messageErr']
    if 'messageOk' in request.session:
        context.update({"messageOk": request.session['messageOk']})
        del request.session['messageOk']
    
def preprocessDataset(request):
    context = {}
    if request.method == "POST" and request.POST['datasetName']:
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dataSetsDir = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")
            if not os.path.exists(os.path.join(dataSetsDir,request.POST['datasetName'])):
                request.session['messageErr'] = "The requested dataset does not exist"
                return redirect('listDatasets')
            else:
                toRet = preprocessing.preprocessDataset(request.POST, dataSetsDir)
                context.update(toRet)
                request.session['messageOk'] = "The preprocessing has been executed correctly"
        except:
            request.session['messageErr'] = "An error occurred preprocessing the DataSet"
            return redirect('listDatasets')
    
    return showDatasetSample( request=request, fileName=context['datasetName'], oldContext=context)




def principalComponentAnalysis(request):
    context = {}
    if request.method == "POST" and request.POST['datasetName']:
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dataSetsDir = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")
            if not os.path.exists(os.path.join(dataSetsDir,request.POST['datasetName'])):
                request.session['messageErr'] = "The requested dataset does not exist"
                return redirect('listDatasets')
            else:
                toRet = preprocessing.principalComponentAnalysis(request.POST, dataSetsDir)
                context.update(toRet)
                request.session['messageOk'] = "The principal Component Analysis has been executed correctly whith a variance ratio of " + str(context["variance_ratio"]) + "%"
        except Exception as e:
            print(str(e))
            request.session['messageErr'] = "An error occurred while executing the principal Component Analysis of the DataSet"
            return redirect('listDatasets')
    
    return showDatasetSample( request=request, fileName=context['datasetName'], oldContext=context)


@login_required(login_url='/login/')
def selectDataset(request):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")

    context = {}

    if not os.path.exists(dataSetsPath):
        context.update({'secondaryMessageWarning': "You haven't any dataset yet"})
    else:
        datasets = []
        for file in os.listdir(dataSetsPath):
            filepath = os.path.join(dataSetsPath, file)
            if os.path.isfile(filepath):
                datasets.append({
                    "name": file,  
                    "creationDate": time.ctime(os.path.getctime(filepath)), 
                    "size": convert_size(os.path.getsize(filepath))})
                         
        context.update({'datasets': datasets})
    
    loadContextMessages(request,context)
    
    return render(request, 'ENNApp/selectDataSet.html', context)