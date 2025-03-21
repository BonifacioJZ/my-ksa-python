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
        cart = self.cart
        qty_in_cart = float(cart[id]['qty']) if id in cart else 0
        total_qty = qty_in_cart + qty
        if total_qty > product.stock:
            return False
        else:
            cart[id] = {
                'id':id,
                'name':product.name,
                'benefit':product.product.name,
                'sku':product.sku,
                'price':str(product.price),
                'qty':total_qty,
                'total':str(float(product.price) * total_qty)
            }
        
        self.save_cart()
        return True
                
    def save_cart(self):
        self.session['cart']=self.cart
        self.session.modified = True
    
    def remove(self,product:Benefit):
        id = str(product.id)
        if id in self.cart:
            del self.cart[id]
            self.save_cart()
    
    def subtract(self,product:Benefit,qty):
        id = str(product.id)
        if id in self.cart:
            actual_qty = float(self.cart[id]['qty'])
            new_qty = actual_qty - float(qty)   
            if new_qty <= 0:
                del self.cart[id]
            else:
                self.cart[id]['qty']= new_qty
                self.cart[id]['total'] = str(float(product.price) * new_qty)
            self.save_cart()
            return True
        else:
            return False
            
    
    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        