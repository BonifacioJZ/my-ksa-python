from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from src.sales.models import Sale
from .models import SalesReturn, SalesReturnDetail
# Create your views here.


class CreateSaleReturnView(TemplateView):
    template_name = "sales_returns/form.html"
    
    def get(self, request, pk=None, *args, **kwargs):
        sale = Sale.objects.filter(id=pk).first()
        if not sale:
            messages.error(request, "No se encontro la venta")
            return redirect("sales:index")
        context = {
            "sale": sale,
            "title": "Devolucion",
            "items":  sale.sales.all(),
            "client": sale.client,
        }
        return render(request, self.template_name, context)
