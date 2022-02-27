''' Views to manage and render the profiles pages '''

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from checkout.models import Order

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    ''' Display the user's profile information '''

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Update the form with the post data
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Something went wrong \
                                     Please make sure information are valid'
                                    'or contact us for assiatance.')
            redirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=user_profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def order_history(request):
    '''
    View to display order history, file for issue and check issue status
    '''
    user_profile = get_object_or_404(UserProfile, user=request.user)
    orders = user_profile.orders.all()
    orders = orders.order_by('-date')

    template = 'profiles/order_history.html'
    context = {
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def view_past_order_history(request, order_number):
    ''' View that display the past, saved order '''
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. \
        A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_order_history': True,
    }

    return render(request, template, context)
