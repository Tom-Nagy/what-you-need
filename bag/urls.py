''' Urls configuration for the bag app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.view_bag, name='view_bag'),
]
