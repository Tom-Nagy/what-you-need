''' Admin configuration and registration for checkout app '''

from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    ''' Allow access to line items of an order from the Order interface '''

    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    ''' Customise the admin Order interface '''

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'order_total', 'delivery_cost',
                       'product_count', 'discount', 'grand_total',
                       'original_bag', 'stripe_pid',)

    fields = ('order_number', 'user_profile', 'date', 'full_name', 'email',
              'phone_number', 'street_address1', 'street_address2', 'postcode',
              'town_or_city', 'county_or_region', 'country', 'product_count',
              'order_total', 'delivery_cost', 'discount', 'grand_total',
              'original_bag', 'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name', 'email',
                    'order_total', 'delivery_cost', 'discount',
                    'grand_total',)

    ordering = ('-date', 'user_profile',)


admin.site.register(Order, OrderAdmin)
