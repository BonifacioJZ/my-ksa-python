from django.shortcuts import redirect,render
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BrandForms
# Create your views here.

#Zona de vistas para Brand
class BrandListView(ListView):
    template_name="brand/index.html"
    model = BrandForms.Meta.model
    context_object_name="brand_list"
    queryset=BrandForms.Meta.model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Marcas"
        return context
    
    
