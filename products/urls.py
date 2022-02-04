''' Urls configuration for the products app '''

from django.urls import path
from . import views


# empty path to indicate the root url
urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]
