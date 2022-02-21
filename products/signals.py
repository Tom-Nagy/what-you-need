'''
Configure signals that listen for the creation of a review
'''

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProductReview


@receiver(post_save, sender=ProductReview)
def update_on_save(sender, instance, created, **kwargs):
    ''' Update order total on lineitem update/create event '''
    instance.product.update_rating()
