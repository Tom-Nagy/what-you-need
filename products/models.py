from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    '''Model that determine how the data will be store for a category'''

    class Meta:
        '''Set verbose name'''
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    for_registered_user = models.BooleanField(default=False)

    def __str__(self):
        ''' String method to return the name of the category '''
        return str(self.name)

    def get_friendly_name(self):
        ''' Return the friendly name of the category '''
        return self.friendly_name


class Product(models.Model):
    '''Model that determine how the data will be store for a product '''
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)], null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)])
    date_added = models.DateTimeField(auto_now_add=True)
    new_product = models.BooleanField(default=False, null=True, blank=True)
    on_sale = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        ''' String method to return the name of the Product '''
        return str(self.name)
