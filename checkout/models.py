''' Models configuration for checkout app '''

import uuid

from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    '''Model that determine how the data will be store for an order'''
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county_or_region = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    product_count = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(0)], null=False, default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2,
                                   null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False,
                                  blank=False, default='')

    def _generate_order_number(self):
        '''Generate a random, unique order number using UUID'''
        return uuid.uuid4().hex.upper()

    def update_total(self):
        '''
        Update grand total each time a line item is added,
        accounting for delivery coast and discount.
        '''
        # or 0, prevent error if we manually delete all the lines items
        # because it would set it to none
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.delivery_cost = self.order_total * settings.DELIVERY_COST/100
        self.product_count = self.lineitems.aggregate(
            Sum('quantity'))['quantity__sum'] or 0

        # create a list of prices of each individual product
        # to determine the discount amount.
        product_price_list = []
        free_product_count = 0
        free_products = []

        for item in self.lineitems.all():
            for x in range(int(item.quantity)):
                product_price_list.append(item.product.price)
        product_price_list.sort()

        # Every 3 items purchase the least expensive is offered.
        # From the list of product prices return a list of prices to discount.
        if self.product_count / 3 >= 1:
            free_product_count = int(self.product_count / 3)
            # Sorted() method from [venpa](https://stackoverflow.com/questions/
            # 22117834/how-do-i-return-a-list-of-the-3-lowest-values-in-another-list)
            free_products = sorted(product_price_list)[:free_product_count]
        else:
            free_product_count = 0

        # Calculate the total discount
        discount = 0
        for prod in free_products:
            discount += Decimal(prod)

        self.discount = discount
        self.grand_total = (self.order_total + self.delivery_cost
                            - self.discount)
        self.save()

    def save(self, *args, **kwargs):
        '''
        Override the original save method to set the order number
        if it hasn't been set already.
        '''
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        ''' String method to return the order number '''
        return self.order_number


class OrderLineItem(models.Model):
    '''Model related to Order and Product, created for each item in the bag'''
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)], null=False, blank=False)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        '''
        Override the original save method to set the lineitem total
        and update the order total.
        '''
        self.lineitem_total = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        ''' String method to return the order number '''
        return f'Item {self.product.name} on order {self.order.order_number}'
