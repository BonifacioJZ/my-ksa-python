from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ClientForms
# Create your views here.

class ClientListView(LoginRequiredMixin, ListView):
    """
    Vista basada en clase para listar los clientes.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
        queryset (QuerySet): Conjunto de objetos a listar, ordenados por nombre.
    """
    template_name = "clients/index.html"
    model = ClientForms.Meta.model
    context_object_name = 'clients_list'
    queryset = model.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Vista basada en clase para crear un nuevo cliente.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        form_class (Form): Formulario a utilizar para crear el cliente.
        success_url (str): URL a la cual redirigir después de crear el cliente.
    """
    template_name = "clients/form.html"
    model = ClientForms.Meta.model
    form_class = ClientForms
    success_url = reverse_lazy('client_index')
    
    def form_valid(self, form) -> HttpResponse:
        """
        Maneja el formulario válido para crear un nuevo cliente.

        Args:
            form (Form): Formulario validado.

        Returns:
            HttpResponse: Redirige a la URL de éxito.
        """
        messages.success(self.request, 'Cliente creado con éxito')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Cliente"
        return context
