''' Urls configuration for the wishlists app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.all_wishlist, name='all_wishlist'),
]
