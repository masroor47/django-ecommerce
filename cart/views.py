from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product
from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'store/cart/summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)

        cartqty = cart.__len__()
        response = JsonResponse({
            'qty': cartqty
        })
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)
        response = JsonResponse({'Success': True})
        return response

