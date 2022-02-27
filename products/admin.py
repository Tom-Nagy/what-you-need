''' Admin configuration and registration for Products app '''

from django.contrib import admin
from .models import Product, Category, ProductReview


class ProductReviewAdmin(admin.ModelAdmin):
    ''' Allow access to all reviews from admin '''

    model = ProductReview

    readonly_fields = ('date_time', 'user', 'content', 'review_rating',
                       'product',)

    list_display = ('date_time', 'user', 'product',
                    'content', 'review_rating',)

    ordering = ('-date_time', 'product',)


class ProductReviewAdminInline(admin.TabularInline):
    ''' Allow access to review of product from the Product admin '''

    model = ProductReview

    readonly_fields = ('date_time', 'user', 'content', 'review_rating',)

    list_display = ('date_time', 'user', 'content', 'review_rating',)

    ordering = ('-date_time',)


class ProductAdmin(admin.ModelAdmin):
    ''' Customise the admin Product interface '''

    inlines = (ProductReviewAdminInline,)
    readonly_fields = ('quantity_sold', 'rating',)
    exclude = ('liked',)

    list_display = (
        'name',
        'category',
        'quantity',
        'price',
        'on_sale',
        'on_sale_price',
        'rating',
        'date_added',
        'image',
        'quantity_sold',
    )

    ordering = ('name', 'category',)


class CategoryAdmin(admin.ModelAdmin):
    ''' Customise the admin Category interface '''
    list_display = (
        'name',
        'friendly_name',
        'for_registered_user',
        'image',
        'selectable',
    )


# Models registration with relevant classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
