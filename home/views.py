'''
View to manage and render the home page,
terms and conditions and contact us form.
'''

from django.shortcuts import render

from contact.forms import ContactUsForm


def index(request):
    ''' A view to return the index page '''

    contact_form = ContactUsForm()

    template = 'home/index.html'
    context = {
        'on_home_page': True,
        'contact_form': contact_form,
    }
    return render(request, template, context)


def terms_and_conditions(request):
    ''' A view to return the terms and conditions page '''

    template = 'home/terms_and_conditions.html'
    context = {
        'on_home_page': True,
    }
    return render(request, template, context)
