''' Views to manage and render the profiles pages '''

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


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

    form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)
