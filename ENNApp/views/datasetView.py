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
    deleteDataSetUrl = "/deleteDataset/" + request.user.username + "/" #ToDO Cambiar a todos para Admin

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataSetsPath = os.path.join(BASE_DIR, "userFiles", request.user.username , "datasets")
    
    #datasets = [f for f in os.listdir(dataSetsPath) if os.path.isfile(os.path.join(dataSetsPath, f))]
    datasets = []
    for file in os.listdir(dataSetsPath):
        filepath = os.path.join(dataSetsPath, file)
        if os.path.isfile(filepath):
            datasets.append({"name": file, "creationDate": time.ctime(os.path.getctime(filepath)), "size": convert_size(os.path.getsize(filepath)), "url": ( downloadDataSetUrl + file), "deleteUrl": deleteDataSetUrl + file + "/"})
    context = {'datasets': datasets}
    
    loadContextMessages(request,context)
    
    return render(request, 'ENNApp/listDataset.html', context)
    #return HttpResponse(' <a href="' + dataSetUrl + '">Login Page</a>')


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



def loadContextMessages(request,context):
    if 'messageErr' in request.session:
        context.update({"messageErr": request.session['messageErr']})
        del request.session['messageErr']
    if 'messageOk' in request.session:
        context.update({"messageOk": request.session['messageOk']})
        del request.session['messageOk']