''' Urls configuration for the contact app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.contact_us, name='contact_us'),
    path('message_received/', views.message_received, name='message_received'),
]
