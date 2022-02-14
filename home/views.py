''' View to manage and render the home page '''
from django.shortcuts import render


def index(request):
    ''' A view to return the index page '''
    on_home_page = True
    context = {
        'on_home_page': on_home_page,
    }
    return render(request, 'home/index.html', context)
