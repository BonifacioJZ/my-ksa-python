from django.http import HttpRequest
def total_cart(request:HttpRequest):
    total =0.0
    if request.user.is_authenticated:
        if 'cart' in request.session:
            cart = request.session['cart']
            for key,value in cart.items():
                total += float(value['total'])
    return {'total_cart':total}