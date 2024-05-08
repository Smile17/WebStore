from django.contrib import admin
from django.urls import path
from cinema_store import views

urlpatterns = [
    path('', views.index, name='home'),
    #path('store', views.store, name='store'),
]