''' View to manage contact us form '''

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.safestring import mark_safe

from profiles.models import UserProfile
from .forms import ContactUsForm
from .models import ContactUs


@require_POST
def contact_us(request):
    ''' Send message to store owner '''

    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST, request.FILES)
        if contact_form.is_valid():
            cust_message = contact_form.save(commit=False)
            if request.user.is_authenticated:
                user_profile = UserProfile.objects.get(
                               user__username=request.user)
                cust_message.user = user_profile
            cust_message.save()

            messages.success(request,
                             mark_safe('Thank you for your message,<br/>'
                                       'an email confirmation was sent to '
                                       f'{cust_message.sender}'))

        return redirect('home')


def message_received(request):
    ''' Display message received '''

    cust_messages = ContactUs.objects.all()

    template = 'contact/message_received.html'
    context = {
        'cust_messages': cust_messages,
    }

    return render(request, template, context)
