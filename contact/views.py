''' View to manage contact us form '''

from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.safestring import mark_safe

from contact.forms import ContactUsForm
from profiles.models import UserProfile


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
