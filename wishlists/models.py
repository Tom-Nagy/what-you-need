''' Models configuration for wishlists app '''

from django.db import models

from profiles.models import UserProfile
from products.models import Product


class Wishlist(models.Model):
    ''' Model for saving user prefered products by category '''

    user = models.ForeignKey(UserProfile, null=False, blank=False,
                             on_delete=models.CASCADE,
                             related_name='wishlist')
    name = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        ''' String method to return the name of the category '''
        return str(self.name)


class WishlistItem(models.Model):
    '''Model for items in a wishlist '''
    wishlist = models.ForeignKey(Wishlist, null=False, blank=False,
                                 on_delete=models.CASCADE,
                                 related_name='wishlist_items')
    product = models.ForeignKey(Product, null=True, blank=True,
                                on_delete=models.SET_NULL)


# @receiver(post_save, sender=Wishlist)
# def create_or_update_default_wishlist(sender, instance, created, **kwargs):
#     """
#     Create a default wishlist or update it.
#     """
#     if created:
#         Wishlist.objects.create()
#     # Existing wishlist: save the wishlist
#     instance.whislist.save()