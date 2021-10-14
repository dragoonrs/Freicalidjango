from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'juroComposto'
urlpatterns = [
    #path('', views.index, name='index'),
    #path('<int:igpm_id>/', views.detail, name='detail'),
    #path('updateIgpm/<int:igpm_id>/', views.updateIgpm, name='updateIgpm'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('updateIgpm/<int:igpm_id>/', views.updateIgpm, name='updateIgpm'),
    path('juroCompostoTable/', views.juroCompostoTable, name='juroCompostoTable'),
    path("upload/", views.upload, name="upload")
]