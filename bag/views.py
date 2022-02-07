''' Views to manage and render the bag pages '''
from django.shortcuts import render


def view_bag(request):
    ''' A view that return the bag content '''
    return render(request, 'bag/bag.html')
