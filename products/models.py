''' Models configuration for Products app '''

from django.db import models
from django.db.models import Sum

from django.core.validators import MinValueValidator, MaxValueValidator

from profiles.models import UserProfile


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
    '''Model that determine how the data will be stored for a product '''
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    scientific_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    height = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(200),
            MinValueValidator(1)], null=True, blank=True)
    diameter = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(200),
            MinValueValidator(1)], null=True, blank=True)
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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    on_sale = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' String method to return the name of the Product '''
        return str(self.name)

    def update_rating(self):
        ''' Update product rating each time a review is added '''
        reviews_nb = self.reviews.count()
        rating_sum = self.reviews.aggregate(
            Sum('review_rating'))['review_rating__sum'] or 0
        
        if reviews_nb > 0:
            self.rating = int(rating_sum / reviews_nb)
        else:
            self.rating = 0
        self.save()


class ProductReview(models.Model):
    '''Model that determine how the data will be store for a review'''

    rating_options = [
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        ]

    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                             null=True, blank=True,)
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    review_rating = models.PositiveSmallIntegerField(
        choices=rating_options,
        default=5,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)],
        null=False, blank=False)
    content = models.TextField(max_length=1000, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        ''' String method to return the name of the Product '''
        return str(self.product.name)
