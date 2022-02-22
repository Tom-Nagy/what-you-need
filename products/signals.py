'''
Configure signals that listen for the creation of a review
'''

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ProductReview


@receiver(post_save, sender=ProductReview)
def update_rating_on_save(sender, instance, created, **kwargs):
    ''' Update rating  when adding a review '''
    instance.product.update_rating()


@receiver(post_delete, sender=ProductReview)
def update_rating_on_delete(sender, instance, **kwargs):
    ''' Update rating  when deleting a review '''
    instance.product.update_rating()
