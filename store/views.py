from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.



def product_all(request):
    products = Product.products.all()
    context = {
        'products': products
    }
    return render(request, 'store/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {
        'product': product
    }
    return render(request, 'store/single.html', context)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/category.html', context)