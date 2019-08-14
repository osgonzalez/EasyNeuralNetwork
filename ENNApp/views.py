from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404


# Import Models
from .models import Question


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
