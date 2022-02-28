''' Urls configuration for the home app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.index, name='home'),
    path('terms_and_conditions/', views.terms_and_conditions,
         name='terms_and_conditions'),
]
