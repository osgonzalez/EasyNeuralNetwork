from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prueba/<int:numero>', views.vistaPrueba, name='vistaPrueba'),
    path('<int:question_id>/', views.detail, name='detail'),

]