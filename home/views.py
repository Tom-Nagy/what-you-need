''' View to manage and render the home page '''
from django.shortcuts import render


def index(request):
    ''' A view to return the index page '''
    context = {
        'on_home_page': True,
    }
    return render(request, 'home/index.html', context)
