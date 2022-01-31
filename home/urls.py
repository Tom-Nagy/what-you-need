from django.contrib import admin
from django.urls import path, include
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.index, name='home'),
]
