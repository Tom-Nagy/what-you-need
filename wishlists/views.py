''' Views to manage and render the wishlists pages '''

from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
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
    liked_product = get_object_or_404(Product, pk=product_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        wishlist = None

        # if no wishlist owned/created
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
            # check if the product is already in the wishlist
            wishlist_items = wishlist.wishlist_items.all()
            for item in wishlist_items:
                if item.product == liked_product:
                    messages.info(request, f'{liked_product} already in \
                                             {wishlist}')
                    return redirect(redirect_url)

        # Add the product to the wishlist
        wishlist_item = WishlistItem()
        wishlist_item.wishlist = wishlist
        wishlist_item.product = liked_product
        wishlist_item.name = liked_product.name
        wishlist_item.save()

        # Delete the product from the bag
        if 'delete_product' in request.POST:
            item_id = request.POST.get('delete_product')
            bag = request.session.get('bag', {})
            bag_item_quantity = 0

            if item_id in list(bag.keys()):
                bag_item_quantity = bag[item_id]

                liked_product.quantity += bag_item_quantity
                liked_product.save()
                bag.pop(item_id)

                messages.success(request, f'{liked_product.name} \
                                            moved to {wishlist}')
                request.session['bag'] = bag
                return redirect('view_bag')
            else:
                messages.error(request,
                                'It seems that we can\'t move this plant!'
                                'If you need assistance, please contact us')
                redirect(reverse('view_bag'))

        else:
            messages.success(request, f'{liked_product.name} saved \
                                        to {wishlist.name}')
            return redirect(redirect_url)

    return redirect(redirect_url)


@login_required
def remove_from_wishlist(request, item_id):
    ''' Delete the selected item from the wishlist '''
    if request.method == 'POST':
        wishlist_item = get_object_or_404(WishlistItem, pk=item_id)
        wishlist_item.delete()
        messages.success(request, f'{wishlist_item} removed from \
                                    {wishlist_item.wishlist}')
        return redirect('all_wishlist')

    return redirect(reverse('all_wishlist'))
