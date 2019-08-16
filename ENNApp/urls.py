from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('testForm', views.testForm, name='testForm'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('testPost/', views.testPost, name='testPost'),
    #------------------------------------------------------
    path('index/', views.index, name='index'),
    path('uploadView/', views.uploadView, name='uploadView'),
    path('addDataset/', views.addDataset, name='addDataset'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)