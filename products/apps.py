''' App configuration '''
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    ''' products app configuration '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        '''
        Override the ready method and import signals module
        '''
        import products.signals
