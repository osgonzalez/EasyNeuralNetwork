from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings




# Import Models
from .models import Question, DataSet


# Views 


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def vistaPrueba(request, numero):
    context = {
        'number': numero,
    }
    return render(request, 'ENNApp/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'ENNApp/detail.html', {'question': question})


def testPost(request):
    test= request.POST["uname"]
    print("stop")

    if request.POST["uname"] == "1" :
        return HttpResponseRedirect(reverse('index', args=(1,)))
    else:
        return HttpResponse("oks -> user: "+ request.POST["uname"] + " pass: " + request.POST["upass"] )


def testForm(request):
    context = {
        'number': 23,
    }
    return render(request, 'ENNApp/index.html', context)

#-------------------------------------------------------------------------------------------#

def uploadView(request):
    return render(request, 'ENNApp/upload.html')

def addDataset(request):
    if request.method == "POST" and request.FILES['dataSet']:
        dataSetFile = request.FILES["dataSet"]
        fileSystem = FileSystemStorage()
        filename = fileSystem.save(dataSetFile.name, dataSetFile)
        #print(dataSetFile.name)
        #print(dataSetFile.size)
    return HttpResponse("oks")
'''
if request.method == 'POST' and request.FILES['dataSet']:
    dataSetFile = request.FILES["dataSet"]
    fileSystem = FileSystemStorage()
    filename = fileSystem.save(dataSetFile.name, dataSetFile)
    uploaded_file_url = fileSystem.url(filename)
    return render(request, 'core/simple_upload.html', {
        'uploaded_file_url': uploaded_file_url
    })
return render(request, 'core/simple_upload.html')
'''
