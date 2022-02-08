''' Urls configuration for the bag app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>', views.add_to_bag, name='add_to_bag'),
]
