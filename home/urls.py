''' Urls configuration for the home app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.index, name='home'),
]
