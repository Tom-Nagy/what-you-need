''' Views to manage and render the products pages '''
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    ''' A view to display all products, including sorting and searching. '''

    products = Product.objects.all()
    query = None
    category_selected = None
    sort = None
    direction = None

    if request.GET:

        # Sorting products
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # Search by category functionality
        if 'category' in request.GET:
            category_selected = request.GET['category']
            products = products.filter(category__name=category_selected)
            # category_selected = Category.objects.filter(
            #                      name=category_selected)
            print(category_selected)

        # Search bar functionality
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You are searching for nothing! \
                                         Try with something!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                      scientific_name__icontains=query) | Q(
                          description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        # 'search_term': query,
        'category_selected': category_selected,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    ''' A view to display details of individual product. '''

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
