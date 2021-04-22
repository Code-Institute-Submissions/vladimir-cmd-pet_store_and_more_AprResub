from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

# Create your views here.
def specific_products_dog(request):
    print('Starting with the function')
    
    try:
        categories = Category.objects.all()
        products = Product.objects.all()
        print('Get the products: {}'.format(products))
        print('Get the categories: {}'.format(categories))
    except Exception as e:
        print('There was an issue with bloody category: {}'.format(str(e)))
    
    print('We are in get request')
    try:
        # if 'dry_dog_food' in categories:
        print('We are in dog check')
        categories = Category.objects.filter(name__contains='dog')
        print(categories)
        products = products.filter(category__name__contains='dog')
        print(products)
    except Exception as e:
        print('There was an issue with enumrating: {}'.format(str(e)))

    context = {
        'products': products,
        'current_categories': categories,
    }
    return render(request, 'products/specific_products_dog.html', context)
   

def specific_products_cat(request):
    print('Starting with the function')
    
    try:
        categories = Category.objects.all()
        products = Product.objects.all()
        print('Get the products: {}'.format(products))
        print('Get the categories: {}'.format(categories))
    except Exception as e:
        print('There was an issue with bloody category: {}'.format(str(e)))
    
    print('We are in get request')
    try:
        # if 'dry_dog_food' in categories:
        print('We are in cat check')
        categories = Category.objects.filter(name__contains='cat')
        print(categories)
        products = products.filter(category__name__contains='cat')
        print(products)
    except Exception as e:
        print('There was an issue with enumrating: {}'.format(str(e)))

    context = {
        'products': products,
        'current_categories': categories,
    }
    return render(request, 'products/specific_products_cat.html', context)
   

def specific_products_bird(request):
    print('Starting with the function')
    
    try:
        categories = Category.objects.all()
        products = Product.objects.all()
        print('Get the products: {}'.format(products))
        print('Get the categories: {}'.format(categories))
    except Exception as e:
        print('There was an issue with bloody category: {}'.format(str(e)))
    
    print('We are in get request')
    try:
        # if 'dry_dog_food' in categories:
        print('We are in bird check')
        categories = Category.objects.filter(name__contains='bird')
        print(categories)
        products = products.filter(category__name__contains='bird')
        print(products)
    except Exception as e:
        print('There was an issue with enumrating: {}'.format(str(e)))

    context = {
        'products': products,
        'current_categories': categories,
    }
    return render(request, 'products/specific_products_bird.html', context)


def specific_products_dealz(request):
    print('Starting with the function')
    
    try:
        categories = Category.objects.all()
        products = Product.objects.all()
        print('Get the products: {}'.format(products))
        print('Get the categories: {}'.format(categories))
    except Exception as e:
        print('There was an issue with bloody category: {}'.format(str(e)))
    
    print('We are in get request')
    try:
        # if 'dry_dog_food' in categories:
        print('We are in bird check')
        categories = Category.objects.filter(name__in=['deals','clearance','new_items'])
        print(categories)
        products = products.filter(category__name__in=['deals','clearance','new_items'])
        print(products)
    except Exception as e:
        print('There was an issue with enumrating: {}'.format(str(e)))

    context = {
        'products': products,
        'current_categories': categories,
    }
    return render(request, 'products/specific_products_dealz.html', context)
   

def all_products(request):
    """ A view to return the index page """
    print("In all products")
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'price':
                if direction == 'asc':
                    sortkey = 's_price'
                else:
                    sortkey = 'x_price'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product page """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have enough permissions to add product. Please contact administrator.")
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have enough permissions to add product. Please contact administrator.")
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure that form is valid.')
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
    if not request.user.is_superuser:
        messages.error(request, "You don't have enough permissions to add product. Please contact administrator.")
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
