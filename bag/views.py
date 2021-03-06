''' Views to manage and render the bag pages '''
from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.contrib import messages

from products.models import Product
from profiles.models import UserProfile


def view_bag(request):
    ''' A view that return the bag contents page '''

    products = Product.objects.all()
    # Reset all the product's liked filed to False
    for product in products:
        product.liked = False
        product.save()

    user_profile = None
    user_wishlist = None
    need_new_queryset = False
    # Get user profile and associated wishlist
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user__username=request.user)
        user_wishlist = user_profile.wishlist.all()

        # check for saved products in a user's wishlist
        # and update liked field accordingling
        if user_wishlist:
            for wishlist in user_wishlist:
                wishlist_items = wishlist.wishlist_items.all()
                if wishlist_items:
                    for item in wishlist_items:
                        if item.product:
                            product_id = item.product.id
                            if product_id:
                                liked_product = \
                                    Product.objects.get(id=product_id)
                                liked_product.liked = True
                                liked_product.save()

                                need_new_queryset = True

    if need_new_queryset:
        # Get the updated query set
        products = Product.objects.all()

    template = 'bag/bag.html'
    context = {
        'on_bag_page': True,
        'user_profile': user_profile,
        'user_wishlist': user_wishlist,
    }
    return render(request, template, context)


def add_to_bag(request, item_id):
    ''' Add a quantity of a specified product to the shopping bag '''

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if quantity <= product.quantity and quantity > 0:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            product.quantity -= quantity
            product.save()
            messages.success(request,
                             f'Added {quantity} more {product.name}'
                             'to your bag', extra_tags='bag_item_qty_changed')
        else:
            bag[item_id] = quantity
            product.quantity -= quantity
            product.save()
            messages.success(request,
                             f'{quantity} {product.name} added to your bag',
                             extra_tags='bag_item_qty_changed')
    else:
        messages.error(request,
                       f'The quantity selected for {product.name}'
                       'is not available')
        return redirect(redirect_url)

    request.session['bag'] = bag
    if 'buy_now' in request.POST:
        return redirect('view_bag')
    else:
        return redirect(redirect_url)


def adjust_bag(request, item_id):
    '''
    Adjust the quantity of the specified product
    to the specified/possible amount in the shopping bag.
    Update the product quantity(stock).
    '''

    product = get_object_or_404(Product, pk=item_id)
    requested_quantity = int(request.POST.get('quantity'))
    available_quantity = product.quantity
    bag = request.session.get('bag', {})
    bag_item_quantity = 0

    if item_id in list(bag.keys()):
        bag_item_quantity = bag[item_id]
    else:
        messages.error(request,
                       'It seems that this item is not in your bag \
                       If you need assistance, please contact us')
        redirect(reverse('view_bag'))

    if requested_quantity < bag_item_quantity:
        dif_qty = bag_item_quantity - requested_quantity
        product.quantity += dif_qty
        product.save()
        bag[item_id] = requested_quantity
        messages.success(request,
                         f'Quantity for {product.name}'
                         f' changed to {requested_quantity}')
    elif requested_quantity > bag_item_quantity:
        dif_qty = requested_quantity - bag_item_quantity
        if available_quantity >= dif_qty:
            product.quantity -= dif_qty
            product.save()
            bag[item_id] = requested_quantity
            messages.success(request,
                             f'Quantity for {product.name}'
                             f' changed to {requested_quantity}')
        else:
            messages.error(request,
                           f'The quantity selected for {product.name}'
                           ' is not available')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    ''' Remove item from the bag '''

    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        bag_item_quantity = 0

        if item_id in list(bag.keys()):
            bag_item_quantity = bag[item_id]
        else:
            messages.error(request,
                           'It seems that this plant is not in your bag \
                           If you need assistance, please contact us')
            redirect(reverse('view_bag'))

        product.quantity += bag_item_quantity
        product.save()
        bag.pop(item_id)

        messages.success(request, f'{product.name} removed from bag')
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing plant: {e}')
        return HttpResponse(status=500)
