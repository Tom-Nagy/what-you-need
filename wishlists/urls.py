''' Urls configuration for the wishlists app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.all_wishlist, name='all_wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<int:list_id>/', views.delete_wishlist,
         name='delete_wishlist'),
    path('edit_wishlist/<int:wishlist_id>/', views.edit_wishlist,
         name='edit_wishlist'),
]
