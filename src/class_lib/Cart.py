from django.http import HttpRequest, HttpResponse
from src.products.models import Benefit
class Cart:
    def __init__(self,request:HttpRequest):
        self.request = request
        self.session = self.request.session
        cart = self.session.get('cart')
        if not cart:
            self.cart=self.session['cart'] = {}
        else:
            self.cart = cart 
    
    def add(self,product:Benefit,qty):
        id = str(product.id)
        if id not in self.cart.keys():
            if qty > product.stock:
                self.cart[id]={
                'product_id':id,
                'name':product.product.name,
                'benefit':product.name,
                'price':str(product.price),
                'qty':product.stock,
                }
            elif qty <= 0:
                self.cart[id]={
                'product_id':id,
                'name':product.product.name,
                'sku':product.sku,
                'benefit':product.name,
                'price':str(product.price),
                'qty':1,
                }
            else:
                self.cart[id]={
                'product_id':id,
                'name':product.product.name,
                'benefit':product.name,
                'price':str(product.price),
                'total':str(product.price*qty),
                'qty':qty,
                }
        else:
            if qty <=0:
                self.cart[id]['qty'] += 1
                self.cart[id]['total'] = str(float(self.cart[id]['price']) * self.cart[id]['qty'])
            else:
                self.cart[id]['qty'] += qty
                self.cart[id]['total'] = str(float(self.cart[id]['price']) * self.cart[id]['qty'])
        self.save_cart()
                
    def save_cart(self):
        self.session['cart']=self.cart
        self.session.modified = True
    
    def remove(self,product:Benefit):
        id = str(product.id)
        if id in self.cart:
            del self.cart[id]
            self.save_cart()
    
    def subtract(self,product:Benefit):
        id = str(product.id)
        if id in self.cart.keys():
            if self.cart[id]['qty'] > 1:
                self.cart[id]['qty'] -= 1
                self.cart[id]['total'] = str(float(self.cart[id]['price']) * self.cart[id]['qty'])
            else:
                self.remove(product)
            self.save_cart()
    
    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        