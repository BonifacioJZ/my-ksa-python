from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ClientForms
# Create your views here.

class ClientListView(LoginRequiredMixin,ListView):
    template_name = "clients/index.html"
    model = ClientForms.Meta.model
    context_object_name = 'clients_list'
    queryset = model.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes" 
        return context

class ClientCreateView(LoginRequiredMixin,CreateView):
    template_name = "clients/form.html"
    model = ClientForms.Meta.model
    form_class = ClientForms
    success_url = reverse_lazy('client_index')
    
    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request,'Cliente creado con exito')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Cliente"
        return context
    
    
