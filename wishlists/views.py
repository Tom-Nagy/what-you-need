''' Views to manage and render the wishlists pages '''

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from profiles.models import UserProfile

from .models import Wishlist, WishlistItem


@login_required
def all_wishlist(request):
    ''' View that display all the wishlists of a user '''
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_wishlist = user_profile.wishlist.all()
    template = 'wishlists/all_wishlist.html'
    context = {
        'all_wishlist': user_wishlist,
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
        if wishlist_name == '':
            messages.error(request, 'Your wishlist name cannot be empty!')
            return redirect('all_wishlist')

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
def edit_wishlist(request, wishlist_id):
    ''' Edit a wishlist name '''

    wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        wishlist_name = request.POST.get('new_wishlist_name')

        if wishlist_name:
            user_wishlist = user_profile.wishlist.all()
            wishlist.name = wishlist_name

            for a_wishlist in user_wishlist:
                if a_wishlist.name == wishlist_name:
                    messages.error(request, f'{wishlist_name} exist aleady. \
                                                Please pick a different name.')
                    return redirect(reverse('edit_wishlist',
                                            args=[wishlist.id]))

            wishlist.save()
            return redirect('all_wishlist')
        else:
            messages.error(request, mark_safe('Something went wrong!<br/> \
                                               Try again or contact us \
                                               for assistance'))
            return redirect(reverse('edit_wishlist',
                                    args=[wishlist.id]))

    return redirect(reverse('all_wishlist'))


@login_required
def delete_wishlist(request, wishlist_id):
    ''' Delete the selected wishlist '''
    wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
    wishlist.delete()

    messages.success(request, 'Wishlist deleted')
    return redirect(reverse('all_wishlist'))


@login_required
def add_to_wishlist(request, product_id):
    '''
    Add a product to a wishlist or to the default wishlist if none created.
    '''
    product = get_object_or_404(Product, pk=product_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        wishlist = None

        # if no wishlist owned
        if 'default_wishlist' in request.POST:
            # create a default wishlit
            wishlist_name = 'wishlist'
            wishlist = Wishlist()
            wishlist.user = user_profile
            wishlist.name = wishlist_name
            wishlist.save()
        else:
            # Get the wishlist
            wishlist_id = request.POST.get('wishlist_id')
            wishlist = get_object_or_404(Wishlist, pk=wishlist_id)

        wishlist_item = WishlistItem()
        wishlist_item.wishlist = wishlist
        wishlist_item.product = product
        wishlist_item.save()
        print(f'wishlist item {wishlist_item}')
        print(f'wishlist item product {wishlist_item.product}')
        print(f'wishlist item product {wishlist.wishlist_items.all()}')
        messages.success(request, f'{product.name} saved to {wishlist.name}')
        return redirect(redirect_url)

    return redirect(reverse('all_products'))
