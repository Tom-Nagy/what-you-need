''' Urls configuration for the profiles app '''

from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('view_past_order_history/<order_number>/',
         views.view_past_order_history, name='view_past_order_history'),
]
