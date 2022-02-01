from django.contrib import admin
from .models import Product, Category

# Models registration
admin.site.register(Product)
admin.site.register(Category)
