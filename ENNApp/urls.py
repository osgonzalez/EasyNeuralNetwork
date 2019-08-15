from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('testForm', views.testForm, name='testForm'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('testPost/', views.testPost, name='testPost'),
    #------------------------------------------------------
    path('uploadView/', views.uploadView, name='uploadView'),
    path('addDataset/', views.addDataset, name='addDataset'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)