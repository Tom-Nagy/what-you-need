''' View to manage contact us form '''

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
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


@login_required
def message_received(request):
    ''' Display message received '''

    cust_messages = ContactUs.objects.all().order_by('-date_time')

    template = 'contact/message_received.html'
    context = {
        'cust_messages': cust_messages,
    }

    return render(request, template, context)


@login_required
def delete_msg(request, msg_id):
    ''' Delete a message from the store '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    msg = get_object_or_404(ContactUs, pk=msg_id)
    msg.delete()

    messages.success(request, 'Message deleted')
    return redirect(reverse('message_received'))
