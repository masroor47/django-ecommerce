from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.

def categories(request):
    return {
        'categories': Category.objects.all()
    }



def all_products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {
        'product': product
    }
    return render(request, 'store/detail.html', context)