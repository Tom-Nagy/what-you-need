''' Urls configuration for the contact app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.contact_us, name='contact_us'),
    path('messages/', views.message_received, name='message_received'),
    path('delete/<int:msg_id>/', views.delete_msg, name='delete_msg'),
]
