''' Views to manage and render the bag pages '''
from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.contrib import messages

from products.models import Product


def view_bag(request):
    ''' A view that return the bag contents page '''
    return render(request, 'bag/bag.html')


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
        else:
            bag[item_id] = quantity
            product.quantity -= quantity
            product.save()
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
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
        print('this item is not in the bag')
        redirect(reverse('view_bag'))

    if requested_quantity < bag_item_quantity:
        dif_qty = bag_item_quantity - requested_quantity
        product.quantity += dif_qty
        product.save()
        bag[item_id] = requested_quantity
    elif requested_quantity > bag_item_quantity:
        dif_qty = requested_quantity - bag_item_quantity
        if available_quantity >= dif_qty:
            product.quantity -= dif_qty
            product.save()
            bag[item_id] = requested_quantity

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
            print('this item is not in the bag')
            redirect(reverse('view_bag'))

        product.quantity += bag_item_quantity
        product.save()
        bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
