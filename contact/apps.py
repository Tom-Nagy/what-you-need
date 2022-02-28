''' App configuration '''
from django.apps import AppConfig


class ContactConfig(AppConfig):
    ''' contact app configuration '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'

    def ready(self):
        '''
        Override the ready method and import signals module
        '''
        import contact.signals
