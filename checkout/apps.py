''' App configuration '''
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    ''' checkout app configuration '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        '''
        Override the ready method and import signals module
        '''
        import checkout.signals
