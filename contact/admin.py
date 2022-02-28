''' Admin configuration and registration for contact app '''

from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    ''' Displayn messages received by customer '''
    model = ContactUs

    readonly_fields = ('date_time', 'subject', 'body',)

    list_display = ('date_time', 'user', 'sender',
                    'subject', 'body',)

    ordering = ('-date_time', 'subject',)


# Models registration with relevant classes
admin.site.register(ContactUs, ContactUsAdmin)
