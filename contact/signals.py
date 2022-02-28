'''
Configure signals that listen for the creation of a message(contact-us)
'''

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactUs


@receiver(post_save, sender=ContactUs)
def update_rating_on_save(sender, instance, created, **kwargs):
    ''' Update rating  when adding a review '''
    instance.confirmation_email_message_received()
