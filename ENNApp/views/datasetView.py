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
        #print(dataSetFile.name)
        #print(dataSetFile.size)
    return HttpResponse("oks")

@login_required(login_url='/login/')
def listDatasets(request):
    dataSetUrl = "/files/" + request.user.username + "/datasets/"

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")
    
    #datasets = [f for f in os.listdir(dataSetsPath) if os.path.isfile(os.path.join(dataSetsPath, f))]
    datasets = []
    for file in os.listdir(dataSetsPath):
        filepath = os.path.join(dataSetsPath, file)
        if os.path.isfile(filepath):
            datasets.append({"name": file, "creationDate": time.ctime(os.path.getctime(filepath)), "size": os.path.getsize(filepath)})
    '''
    '''
    #return HttpResponse(str(onlyfiles))
    return render(request, 'ENNApp/listDataset.html', {'datasets': datasets})
    #return HttpResponse(' <a href="' + dataSetUrl + '">Login Page</a>')