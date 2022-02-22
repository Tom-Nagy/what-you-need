''' Views to manage and render the wishlists pages '''

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required


def all_wishlist(request):
    ''' View that display all the wishlists of a user '''
    template = 'wishlists/all_wishlist.html'
    context = {}
    return render(request, template, context)
