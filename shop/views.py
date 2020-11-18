from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand

# Create your views here.
from django.contrib.auth.decorators import login_required


  
def product_list(request, category_slug=None, brand_slug=None):
    category = None
    brand = None
    query = None
    
    if 'query' in request.GET:
        query = request.GET['query']
        print(query)
       
  
    #pylint: disable=E1101
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    elif query:
        products = products.filter(name__icontains = query)
    elif brand_slug:
        
        products = products.filter(brands__name__contains=brand_slug)

    return render(request, 'shop/product/list.html', {
                                                        'categories': categories,
                                                        'category': category,
                                                        'products': products,
                                                        'brand': brand,
                                                        'query': query
                                                    })
def brand_detail(request, brand_slug):
    brand = None
    print(brand_slug)
    print("hello")
    #pylint: disable=E1101
    brand = get_object_or_404(Brand, id=brand_slug)
    products = Product.objects.filter(available=True)
    products = products.filter(brands=brand)

    return render(request, 'shop/product/list.html', {
        'products': products,
        'brand': brand
    })
def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product, 'categories': categories})


def index(request):
    products = Product.objects.filter(available=True).order_by('-created')
    categories = Category.objects.all()
    latest_product = products[:6]
    return render(request, 'shop/product/index.html', {'categories': categories, 'latest_product': latest_product})


