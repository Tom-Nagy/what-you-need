'''
Context processor to make categories available across the entire application.
'''
from .models import Category


def all_categories(request):
    ''' Provide a list all categories '''
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }
    return context
