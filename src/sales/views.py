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
        print(qty)
    