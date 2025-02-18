from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from .forms import SupplierForm,SupplierContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
class SupplierListView(LoginRequiredMixin, ListView):
    """
    Vista basada en clase para listar los proveedores.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
        queryset (QuerySet): Conjunto de objetos a listar, ordenados por nombre.
    """
    template_name = "supplier/index.html"
    model = SupplierForm.Meta.model
    context_object_name = 'suppliers_list'
    queryset = SupplierForm.Meta.model.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context

class SupplierCreateView(LoginRequiredMixin,CreateView):
    """
    Vista basada en clase para crear un nuevo proveedor.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        form_class (Form): Formulario a utilizar para crear el proveedor.
        success_url (str): URL a la cual redirigir después de una creación exitosa.
    """
    template_name = "supplier/form.html"
    model = SupplierForm.Meta.model
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context
    
    def post(self, request:HttpRequest, *args, **kwargs):
        """
        Maneja la solicitud POST para crear un nuevo proveedor.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        form = SupplierForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message="El Proveedor fue creado exitosamente")
            return redirect(self.success_url)
        context ={
            'form':form
        }
        messages.error(request=request,message="Error al crear el Proveedor")
        return render(request,self.template_name,context)
class SupplierDetailView(LoginRequiredMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de un proveedor.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
        queryset (QuerySet): Conjunto de objetos a listar.
    """
    template_name = "supplier/show.html"
    model = SupplierForm.Meta.model
    context_object_name = 'supplier'
    queryset = SupplierForm.Meta.model.objects.all()
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedor" 
        return context
    
    def get(self, request, slug=None, *args, **kwargs):
        """
        Maneja la solicitud GET para mostrar los detalles de un proveedor.

        Args:
            request (HttpRequest): La solicitud HTTP.
            slug (str): El slug del proveedor.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        supplier = self.queryset.select_related().all().filter(slug=slug).first()
        if supplier:
            return render(request, self.template_name, {'supplier': supplier})
        messages.error(request, message="No Existe el Proveedor")
        return redirect(reverse_lazy("supplier_index"))

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista basada en clase para actualizar un proveedor existente.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        form_class (Form): Formulario a utilizar para actualizar el proveedor.
        success_url (str): URL a la cual redirigir después de una actualización exitosa.
    """
    template_name = "supplier/form.html"
    model = SupplierForm.Meta.model
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Maneja la solicitud POST para actualizar un proveedor existente.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        supplier = self.get_object()
        form = SupplierForm(instance=supplier, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="El Proveedor fue actualizado exitosamente")
            return redirect(self.success_url)
        context = {
            'form': form
        }
        messages.error(request=request, message="Error al actualizar el Proveedor")
        return render(request, self.template_name, context)

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista basada en clase para eliminar un proveedor existente.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        success_url (str): URL a la cual redirigir después de una eliminación exitosa.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
    """
    template_name = "supplier/delete.html"
    model = SupplierForm.Meta.model
    success_url = reverse_lazy('supplier_index')
    context_object_name = "supplier"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context
    
    def get(self, request: HttpRequest, slug=None, *args, **kwargs):
        """
        Maneja la solicitud GET para mostrar la confirmación de eliminación de un proveedor.

        Args:
            request (HttpRequest): La solicitud HTTP.
            slug (str): El slug del proveedor.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        supplier = self.model.objects.filter(slug=slug).first()
        if supplier:
            context = {
                'supplier': supplier
            }
            return render(request, self.template_name, context)
        messages.error(request, message="No Existe el Proveedor")
        return redirect(reverse_lazy("supplier_index"))
    
    def form_valid(self, form):
        """
        Maneja la validación del formulario de eliminación.

        Args:
            form (Form): El formulario de eliminación.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        messages.success(request=self.request, message="El Proveedor se ha eliminado correctamente")
        return super().form_valid(form)

class SupplierContactListView(LoginRequiredMixin,ListView):
    """
    Vista basada en clase para listar los contactos de un proveedor.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
        queryset (QuerySet): Conjunto de objetos a listar, ordenados por nombre.
    """
    template_name = "supplier_contact/index.html"
    model = SupplierContactForm.Meta.model
    context_object_name = 'contacts_list'
    queryset = SupplierContactForm.Meta.model.objects.all().select_related('supplier').order_by('name')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Contactos" 
        return context

class SupplierContactCreateView(LoginRequiredMixin,CreateView):
    """
    Vista basada en clase para crear un nuevo contacto de un proveedor.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        form_class (Form): Formulario a utilizar para crear el contacto.
        success_url (str): URL a la cual redirigir después de una creación exitosa.
    """
    template_name = "supplier_contact/form.html"
    model = SupplierContactForm.Meta.model
    form_class = SupplierContactForm
    success_url = reverse_lazy('supplier_contact_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Contactos" 
        return context
    
    def post(self, request:HttpRequest, *args, **kwargs):
        """
        Maneja la solicitud POST para crear un nuevo contacto de un proveedor.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        form = SupplierContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message="El Contacto fue creado exitosamente")
            return redirect(self.success_url)
        context ={
            'form':form
        }
        messages.error(request=request,message="Error al crear el Contacto")
        return render(request,self.template_name,context)

##TODO Implementar las vistas de detalle de contacto

class SupplierContactUpdateView(LoginRequiredMixin,UpdateView):
    """
    Vista basada en clase para actualizar un contacto de un proveedor existente.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        form_class (Form): Formulario a utilizar para actualizar el contacto.
        success_url (str): URL a la cual redirigir después de una actualización exitosa.
    """
    template_name = "supplier_contact/form.html"
    model = SupplierContactForm.Meta.model
    form_class = SupplierContactForm
    success_url = reverse_lazy('supplier_contact_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Contactos" 
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Maneja la solicitud POST para actualizar un contacto de un proveedor existente.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        contact = self.get_object()
        form = SupplierContactForm(instance=contact, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="El Contacto fue actualizado exitosamente")
            return redirect(self.success_url)
        context = {
            'form': form
        }
        messages.error(request=request, message="Error al actualizar el Contacto")
        return render(request, self.template_name, context)

class SupplierContactDeleteView(LoginRequiredMixin,DeleteView):
    """
    Vista basada en clase para eliminar un contacto de un proveedor existente.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        model (Model): Modelo a utilizar para obtener los datos.
        success_url (str): URL a la cual redirigir después de una eliminación exitosa.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
    """
    template_name = "supplier_contact/delete.html"
    model = SupplierContactForm.Meta.model
    success_url = reverse_lazy('supplier_contact_index')
    context_object_name = "contact"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Contactos" 
        return context
    
    def get(self, request: HttpRequest, slug=None, *args, **kwargs):
        """
        Maneja la solicitud GET para mostrar la confirmación de eliminación de un contacto de un proveedor.

        Args:
            request (HttpRequest): La solicitud HTTP.
            pk (int): La clave primaria del contacto.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        contact = self.model.objects.filter(slug=slug).first()
        if contact:
            context = {
                'contact': contact
            }
            return render(request, self.template_name, context)
        messages.error(request, message="No Existe el Contacto")
        return redirect(reverse_lazy("supplier_contact_index"))
    
    def form_valid(self, form):
        """
        Maneja la validación del formulario de eliminación.

        Args:
            form (Form): El formulario de eliminación.

        Returns:
            HttpResponse: La respuesta HTTP.
        """
        messages.success(request=self.request, message="El Contacto se ha eliminado correctamente")
        return super().form_valid(form)