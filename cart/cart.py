from store.models import Product
from decimal import Decimal


class Cart():
    # Default behaviours that can be inherited or overrided

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    
    def add(self, product, qty):
        product_id = product.id

        if product_id not in self.cart:
            self.cart[product_id] = {
                'price': str(product.price),
                'qty': int(qty)
            }

        self.save()
    
    # product is the id of the product
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
        self.save()
    
    def update(self, product, qty):
        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty

        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item



    def __len__(self):
        '''
        Get cart data and count the qty of items
        '''

        return sum(item['qty'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        

    def save(self):
        self.session.modified = True