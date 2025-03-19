from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SaleForm,SearchProductForm
from src.class_lib.Cart import Cart
from src.products.models import Benefit
# Create your views here.

class SalesCreateView(LoginRequiredMixin,CreateView):
    template_name="sales/index.html"
    form_class=SaleForm
    model=SaleForm.Meta.model
    success_url=reverse_lazy('product_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Ventas"
        
        context["search"] = SearchProductForm()
        return context

def add_product(request:HttpRequest,slug:str):
    cart = Cart(request)
    if request.POST:
        product = Benefit.objects.select_related().filter(slug=slug).first()
        qty = float(request.POST.get('qty'))
        success = cart.add(product,qty)
        if not success:
            messages.error(request,"No hay suficiente stock")
            return render(request,'components/_close_windows.html')
        messages.success(request,"Producto agregado al carrito")
        return render(request,'components/_close_windows.html')

def add_one_product(request:HttpRequest,pk:str):
    cart = Cart(request)
    product = Benefit.objects.select_related().filter(id=pk).first()
    success = cart.add(product,1)
    if not success:
        messages.error(request,"No hay suficiente stock")
        return redirect(reverse_lazy('sales_index'))
    messages.success(request,"Producto agregado al carrito")
    return redirect(reverse_lazy('sales_index'))

def subtract_one_product(request:HttpRequest,pk:str):
    cart = Cart(request)
    product = Benefit.objects.select_related().filter(id=pk).first()
    success = cart.subtract(product,1)
    if not success:
        messages.error(request,"No se encuentra el producto en el carrito")
        return redirect('sales_index')
    messages.success(request,"Se eliminado un elemento  del carrito")
    return redirect('sales_index')
    

def remove_product(request:HttpRequest,pk:str):
    cart = Cart(request)
    product = Benefit.objects.select_related().filter(id=pk).first()
    cart.remove(product)
    messages.success(request,"Producto eliminado del carrito")
    return redirect('sales_index')
    