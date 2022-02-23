''' Views to manage and render the products pages '''
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.safestring import mark_safe

from profiles.models import UserProfile

from .models import Product, Category, ProductReview
from .forms import ProductForm, ProductReviewForm


def all_products(request):
    ''' A view to display all products, including sorting and searching. '''

    products = Product.objects.all()
    query = None
    category_selected = None
    current_category = None
    sort = None
    direction = None

    if request.GET:

        # Sorting products
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                    direction = '(high to low)'
                else:
                    direction = '(low to high)'
            products = products.order_by(sortkey)

        # Search by category functionality
        if 'category' in request.GET:
            category_selected = request.GET['category']
            products = products.filter(category__name=category_selected)
            current_category = Category.objects.filter(
                                 name=category_selected)

        # Search bar functionality
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               mark_safe('You are searching for nothing! \
                                          <br/>Try with something!'))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                      scientific_name__icontains=query) | Q(
                          description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort} {direction}'
    need_sorting = True

    template = 'products/products.html'
    context = {
        'on_product_page': True,
        'products': products,
        'search_term': query,
        'category_selected': category_selected,
        'current_category': current_category,
        'current_sorting': current_sorting,
        'need_sorting': need_sorting,
    }
    return render(request, template, context)


def product_detail(request, product_id):
    ''' A view to display details of individual product. '''

    product = get_object_or_404(Product, pk=product_id)
    review_form = ProductReviewForm()
    reviews = ProductReview.objects.all()

    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user__username=request.user)
        user_wishlist = user_profile.wishlist.all()

    template = 'products/product_detail.html'
    context = {
        'on_product_page': True,
        'user': user_profile,
        'user_wishlist': user_wishlist,
        'product': product,
        'review_form': review_form,
        'reviews': reviews,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    ''' Add a product to the store '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product.'
                                    'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    ''' Edit a product in the store '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to update product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    ''' Delete a product from the store '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect(reverse('products'))


@login_required
def add_review(request, product_id):
    ''' Add a review for a specified product '''

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        redirect_url = request.POST.get('review_redirect_url')

        form = ProductReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = user_profile
            form.save()
            messages.success(request,
                             mark_safe(f'You added a review for {product.name}'
                                       '<br/>Thank you for your feedback!'))
            return redirect(redirect_url)

        else:
            messages.error(request, 'Something went wrong \
                                     Please make sure information are valid'
                                    'or contact us for assiatance.')
            return redirect(reverse('product_detail', args=[product.id]))

    return redirect(reverse('product_detail', args=[product.id]))
