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



# Views 


@login_required(login_url='/login/')
def index(request):
    return render(request, 'ENNApp/index.html', {})

'''
@login_required(login_url='/login/')
def vistaPrueba(request, numero):
    context = {
        'number': numero,
    }
    return render(request, 'ENNApp/index.html', context)


@login_required(login_url='/login/')
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'ENNApp/detail.html', {'question': question})


@login_required(login_url='/login/')
def testPost(request):
    test= request.POST["uname"]
    print("stop")

    if request.POST["uname"] == "1" :
        return HttpResponseRedirect(reverse('index', args=(1,)))
    else:
        return HttpResponse("oks -> user: "+ request.POST["uname"] + " pass: " + request.POST["upass"] )


@login_required(login_url='/login/')
def testForm(request):
    context = {
        'number': 23,
    }
    return render(request, 'ENNApp/index.html', context)
'''
#-------------------------------------------------------------------------------------------#
'''
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
'''


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


def loginUser(request):
    if request.method == "POST" and request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'loginError': True})
    else: 
        return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    if request.method == "POST" and request.POST['username'] and request.POST['password'] and request.POST['userEmail']:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['userEmail']

        if userModel.objects.filter(username=username).exists():
            return render(request, 'register.html', {'registerError': True})
        else:
            newUser = userModel.objects.create_user(username, email, password)
            #newUser.last_name = request.POST['lastName']
            #newUser.first_name = request.POST['firstName']
            #newUser.save()
            return redirect('login')
    else: 
        return render(request, 'register.html')

'''
@login_required(login_url='/login/')
def listDatasets(request):
    dataSetUrl = "/files/" + request.user.username + "/datasets/"

    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataSetsPath = os.path.join(BASE_DIR, str("userFiles/" +  request.user.username + "/datasets/"))
    onlyfiles = [f for f in os.listdir(dataSetsPath) if os.path.isfile(os.path.join(dataSetsPath, f))]
    
    #return HttpResponse(str(onlyfiles))
    return render(request, 'ENNApp/listDataset.html', {'loginError': True})
    #return HttpResponse(' <a href="' + dataSetUrl + '">Login Page</a>')
    '''