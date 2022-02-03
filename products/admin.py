''' Admin configuration and registration for Products app '''

from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    ''' Customise the admin Product interface '''
    list_display = (
        'name',
        'category',
        'quantity',
        'price',
        'on_sale',
        'rating',
        'date_added',
        'image',
    )

    ordering = ('name', 'category',)


class CategoryAdmin(admin.ModelAdmin):
    ''' Customise the admin Category interface '''
    list_display = (
        'name',
        'friendly_name',
        'for_registered_user',
        'image',
    )


# Models registration with relevant classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
