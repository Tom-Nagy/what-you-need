''' Views to manage and render the wishlists pages '''

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from profiles.models import UserProfile

from .models import Wishlist, WishlistItem


@login_required
def all_wishlist(request):
    ''' View that display all the wishlists of a user '''
    wishlist = Wishlist.objects.all()
    template = 'wishlists/all_wishlist.html'
    context = {
        'wishlist': wishlist,
        'on_profile_page': True,
    }
    return render(request, template, context)


@login_required
def add_wishlist(request):
    ''' Add a wishlist '''
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        wishlist_name = request.POST.get('wishlist_name')
        user_wishlist = user_profile.wishlist.all()

        if user_wishlist:
            for wishlist in user_wishlist:
                if wishlist.name == wishlist_name:
                    messages.error(request, f'{wishlist_name} exist aleady. \
                                            Please choose a different name.')
                    return redirect('all_wishlist')

        wishlist = Wishlist()
        wishlist.user = user_profile
        wishlist.name = wishlist_name
        wishlist.save()
        messages.success(request, 'Wishlist created')
        return redirect('all_wishlist')

    return redirect(reverse('all_wishlist'))


@login_required
def delete_wishlist(request, list_id):
    ''' Delete the selected wishlist '''
    wishlist = get_object_or_404(Wishlist, pk=list_id)
    print(f'wishlist to delete {wishlist}')
    wishlist.delete()

    messages.success(request, 'Wishlist deleted')
    return redirect(reverse('all_wishlist'))


# @login_required
# def add_to_wishlist(request, product_id):
#     '''
#     Add a product to a wishlist or to the default wishlist if none created.
#     '''
#     if request.method == 'POST':
#         product = get_object_or_404(Product, pk=product_id)
#         user_profile = get_object_or_404(UserProfile, user=request.user)
#         redirect_url = request.POST.get('redirect_url')
#         wishlist_name = request.POST.get('wishlist_name')

#         wishlist = Wishlist.objects.get(name=wishlist_name)
#         if not wishlist:
#             wishlist = Wishlist.create()
#             wishlist.user = user_profile
#             wishlist.name = 'wishlist'
#             wishlist.save()
#             messages.info(request, f'Wishlist created')
        
#         wishlist  
#         WishlistItem.product = product
#         WishlistItem()
