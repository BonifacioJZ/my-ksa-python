from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BrandForms,ProductForms,BenefitForm
from django.db.models import Q
from django.urls import reverse_lazy
# Create your views here.

#Zona de vistas para Brand
class BrandListView(LoginRequiredMixin, ListView):
    """
    Vista basada en clase para listar las marcas.

    Atributos:
        template_name (str): Nombre de la plantilla a utilizar para renderizar la vista.
        paginate_by (int): Número de objetos a mostrar por página.
        model (Model): Modelo a utilizar para obtener los datos.
        context_object_name (str): Nombre del contexto que se pasará a la plantilla.
        queryset (QuerySet): Conjunto de objetos a listar, ordenados por nombre.
    """
    template_name = "brand/index.html"
    model = BrandForms.Meta.model
    context_object_name = "brand_list"
    queryset = BrandForms.Meta.model.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos adicionales.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Marcas"
        return context

class BrandCreateView(LoginRequiredMixin,CreateView):
    """
    BrandCreateView es una vista de Django para crear nuevas instancias de Brand.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado.
        CreateView: Proporciona la capacidad de crear nuevos objetos.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con el formulario.
        form_class (Form): La clase de formulario utilizada para crear un nuevo Brand.
        queryset (QuerySet): El conjunto de objetos Brand.
        success_url (str): La URL a la que redirigir después de enviar el formulario con éxito.
    Métodos:
        get_context_data(**kwargs):
            Agrega datos adicionales al contexto de la plantilla.
        post(request: HttpRequest, *args, **kwargs):
            Maneja las solicitudes POST, valida el formulario, guarda el nuevo Brand y redirige a la URL de éxito.
    """
    template_name="brand/form.html"
    model=BrandForms.Meta.model
    form_class= BrandForms
    queryset = BrandForms.Meta.model.objects.all()
    success_url=reverse_lazy('brand_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Marcas' 
        return context
    
    def post(self, request:HttpRequest, *args, **kwargs):
        form = BrandForms(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message="La Marca fue creada exitosamente")
            return redirect(self.success_url)
        context ={
            'form':form
        }
        return render(request,self.template_name,context)

class BrandDetailView(LoginRequiredMixin,DetailView):
    """
    BrandDetailView es una vista para mostrar los detalles de una instancia de Brand.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado para acceder a esta vista.
        DetailView: Proporciona la capacidad de mostrar los detalles de un objeto específico.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, derivado de BrandForms.Meta.model.
        queryset (QuerySet): El conjunto de objetos a mostrar.
        context_object_name (str): Nombre de la variable de contexto a utilizar para el objeto que se está mostrando.
    Métodos:
        get_context_data(**kwargs): Agrega datos adicionales al contexto de la plantilla.
        get(request, slug=None, *args, **kwargs): Maneja las solicitudes GET para renderizar la página de detalles.
    """
    template_name="brand/show.html"
    model = BrandForms.Meta.model
    queryset= BrandForms.Meta.model.objects.all()
    context_object_name = "brand"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Marca" 
        return context
    
    def get(self, request,slug=None, *args, **kwargs):
        brand = self.queryset.select_related().all().filter(slug=slug).first()
        if brand:
            context ={
                'brand':brand
            }
            return render(request,self.template_name,context)
        messages.error(request,message="No Existe la Marca")
        return redirect(reverse_lazy("brand_index"))

class BrandUpdateView(LoginRequiredMixin,UpdateView):
    """
    BrandUpdateView es una vista para actualizar instancias de Brand.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado para acceder a esta vista.
        UpdateView: Proporciona la capacidad de actualizar un objeto específico.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, derivado de BrandForms.Meta.model.
        form_class (Form): La clase de formulario utilizada para actualizar el modelo.
        queryset (QuerySet): El conjunto de objetos a actualizar.
        success_url (str): La URL a la que redirigir después de enviar el formulario con éxito.
    Métodos:
        get_context_data(**kwargs): Agrega datos adicionales al contexto de la plantilla.
        form_valid(form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
        form_invalid(form): Maneja los errores de envío del formulario, mostrando un mensaje de error.
    """
    template_name="brand/form.html"
    model = BrandForms.Meta.model
    form_class = BrandForms
    queryset=BrandForms.Meta.model.objects.all()
    success_url=reverse_lazy('brand_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Marca"
        return context
    
    def form_valid(self, form):
        messages.success(self.request,message="La Marca fue actualizada exitosamente")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,message="Error al Actualizar")
        response = super().form_invalid(form)
        return response

class BrandDeleteView(LoginRequiredMixin,DeleteView):
    """
    BrandDeleteView maneja la eliminación de un objeto Brand.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado.
        DeleteView: Proporciona la capacidad de eliminar un objeto específico.
    Atributos:
        template_name (str): Ruta a la plantilla utilizada para renderizar la página de confirmación de eliminación.
        model (Model): El modelo asociado con esta vista.
        success_url (str): URL a la que redirigir después de una eliminación exitosa.
        context_object_name (str): Nombre de la variable de contexto a utilizar para el objeto que se está eliminando.
    Métodos:
        get_context_data(**kwargs): Agrega datos adicionales al contexto de la plantilla.
        get(request, slug=None, *args, **kwargs): Maneja las solicitudes GET para renderizar la página de confirmación de eliminación.
        form_valid(form): Maneja el envío del formulario para eliminar el objeto y muestra un mensaje de éxito.
    """
    template_name="brand/delete.html"
    model=BrandForms.Meta.model
    success_url=reverse_lazy('brand_index')
    context_object_name="brand"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Marca"
        return context
    
    def get(self, request:HttpRequest,slug=None, *args, **kwargs):
        brand = self.model.objects.filter(slug=slug).first()
        if brand :
            context ={
                'brand':brand
            }
            return render(request,self.template_name,context)
        messages.error(request,message="No Existe la marca")
        return redirect(reverse_lazy("brand_index"))
    
    def form_valid(self, form):
        messages.success(request=self.request,message="La marca se a eliminado correctamente")
        return super().form_valid(form)

##Products

class ProductListView(LoginRequiredMixin,ListView):
    """
    ProductListView es una vista basada en clase que muestra una lista de productos.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        ListView: Una vista genérica de Django que renderiza una lista de objetos.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, definido en ProductForms.Meta.model.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar la lista de productos, ordenados por nombre.
        context_object_name (str): El nombre de la variable de contexto que contendrá la lista de productos.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista, incluyendo un título.
    """
    template_name="product/index.html"
    model=ProductForms.Meta.model
    queryset=ProductForms.Meta.model.objects.all().select_related().order_by('name')
    context_object_name="products_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos" 
        return context
    
class ProductCreateView(LoginRequiredMixin,CreateView):
    """
    ProductCreateView es una vista basada en clase que permite crear un nuevo producto.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        CreateView: Una vista genérica de Django que maneja la creación de un nuevo objeto.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, definido en ProductForms.Meta.model.
        form_class (Form): La clase de formulario utilizada para crear un nuevo producto.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar la lista de productos.
        success_url (str): La URL a la que redirigir después de enviar el formulario con éxito.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista.
        form_valid(self, form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
    """
    template_name="product/form.html"
    model=ProductForms.Meta.model
    form_class=ProductForms
    queryset=ProductForms.Meta.model.objects.all()
    success_url=reverse_lazy('product_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El producto se ha guardado correctamente")
        return super().form_valid(form)

class ProductDetailView(LoginRequiredMixin,DetailView):
    """
    ProductDetailView es una vista basada en clase para mostrar los detalles de un producto.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado.
        DetailView: Vista genérica de Django para mostrar detalles.
    Atributos:
        template_name (str): La plantilla para renderizar los detalles del producto.
        model (Model): El modelo asociado con la vista.
        queryset (QuerySet): El conjunto de datos para recuperar las instancias del producto.
        context_object_name (str): El nombre de la variable de contexto para el producto.
    Métodos:
        get_context_data(**kwargs): Agrega datos adicionales al contexto de la plantilla.
        get(request, slug=None, *args, **kwargs): Maneja las solicitudes GET para mostrar los detalles del producto.
    """
    template_name="product/show.html"
    model=ProductForms.Meta.model
    queryset=ProductForms.Meta.model.objects.all()
    context_object_name="product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        return context
    
    def get(self, request:HttpRequest,slug=None, *args, **kwargs):
        product = self.queryset.select_related().all().filter(slug=slug).first()
        if product:
            slug_benefit = request.GET.get('benefit')
            
            if slug_benefit:
                benefit = product.products.all().filter(slug=slug_benefit).first()
            else:
                benefit=product.products.all().first()
            context ={
                'product':product,
                'benefit':benefit,
            }
            return render(request,self.template_name,context)
        messages.error(request,message="No Existe el Producto")
        return redirect(reverse_lazy("product_index"))

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    """
    ProductUpdateView es una vista basada en clase que permite actualizar un producto existente.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        UpdateView: Una vista genérica de Django que maneja la actualización de un objeto existente.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, definido en ProductForms.Meta.model.
        form_class (Form): La clase de formulario utilizada para actualizar el producto.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar las instancias del producto.
        success_url (str): La URL a la que redirigir después de enviar el formulario con éxito.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista.
        form_valid(self, form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
    """
    template_name="product/form.html"
    model=ProductForms.Meta.model
    queryset=ProductForms.Meta.model.objects.all()
    form_class=ProductForms
    success_url=reverse_lazy('product_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El producto se ha actualizado correctamente")
        return super().form_valid(form)
    
class ProductDeleteView(LoginRequiredMixin,DeleteView):
    """
    ProductDeleteView es una vista basada en clase que maneja la eliminación de un producto.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        DeleteView: Una vista genérica de Django que maneja la eliminación de un objeto específico.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la página de confirmación de eliminación.
        model (Model): El modelo asociado con la vista, definido en ProductForms.Meta.model.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar las instancias del producto.
        success_url (str): La URL a la que redirigir después de una eliminación exitosa.
        context_object_name (str): El nombre de la variable de contexto que contendrá el producto a eliminar.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista.
        get(self, request: HttpRequest, slug=None, *args, **kwargs): Maneja las solicitudes GET para renderizar la página de confirmación de eliminación.
        form_valid(self, form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
    """
    template_name="product/delete.html"
    model=ProductForms.Meta.model
    queryset=ProductForms.Meta.model.objects.all()
    success_url=reverse_lazy('product_index')
    context_object_name="product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        return context
    
    def get(self, request:HttpRequest,slug=None, *args, **kwargs):
        product = self.model.objects.filter(slug=slug).first()
        if product :
            context ={
                'product':product
            }
            return render(request,self.template_name,context)
        messages.error(request,message="No Existe el Producto")
        return redirect(reverse_lazy("product_index"))
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El producto se ha eliminado correctamente")
        return super().form_valid(form)
    
class BenefitListView(LoginRequiredMixin,ListView):
    """
    BenefitListView es una vista basada en clase que muestra una lista de beneficios.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        ListView: Una vista genérica de Django que renderiza una lista de objetos.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, definido en BenefitForm.Meta.model.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar la lista de beneficios, ordenados por nombre.
        context_object_name (str): El nombre de la variable de contexto que contendrá la lista de beneficios.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista, incluyendo un título.
    """
    template_name="benefit/index.html"
    model=BenefitForm.Meta.model
    queryset=BenefitForm.Meta.model.objects.all().order_by('name')
    context_object_name="benefits_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Beneficios" 
        return context

class BenefitCreateView(LoginRequiredMixin,CreateView):
    """
    BenefitCreateView es una vista basada en clase que permite crear un nuevo beneficio.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        CreateView: Una vista genérica de Django que maneja la creación de un nuevo objeto.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, definido en BenefitForm.Meta.model.
        form_class (Form): La clase de formulario utilizada para crear un nuevo beneficio.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar la lista de beneficios.
        success_url (str): La URL a la que redirigir después de enviar el formulario con éxito.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista.
        form_valid(self, form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
    """
    template_name="benefit/form.html"
    model=BenefitForm.Meta.model
    form_class=BenefitForm
    queryset=BenefitForm.Meta.model.objects.all()
    success_url=reverse_lazy('benefit_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Beneficios"
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El beneficio se ha guardado correctamente")
        return super().form_valid(form)

class BenefitUpdateView(LoginRequiredMixin,UpdateView):
    """
    BenefitUpdateView es una vista basada en clase que permite actualizar un beneficio existente.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        UpdateView: Una vista genérica de Django que maneja la actualización de un objeto existente.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la vista.
        model (Model): El modelo asociado con la vista, definido en BenefitForm.Meta.model.
        form_class (Form): La clase de formulario utilizada para actualizar el beneficio.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar las instancias del beneficio.
        success_url (str): La URL a la que redirigir después de enviar el formulario con éxito.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista.
        form_valid(self, form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
    """
    template_name="benefit/form.html"
    model=BenefitForm.Meta.model
    queryset=BenefitForm.Meta.model.objects.all()
    form_class=BenefitForm
    success_url=reverse_lazy('benefit_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Beneficios"
        return context
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El beneficio se ha actualizado correctamente")
        return super().form_valid(form)

class BenefitDeleteView(LoginRequiredMixin,DeleteView):
    """
    BenefitDeleteView es una vista basada en clase que maneja la eliminación de un beneficio.
    Hereda de:
        LoginRequiredMixin: Asegura que el usuario esté autenticado antes de acceder a la vista.
        DeleteView: Una vista genérica de Django que maneja la eliminación de un objeto específico.
    Atributos:
        template_name (str): La ruta a la plantilla utilizada para renderizar la página de confirmación de eliminación.
        model (Model): El modelo asociado con la vista, definido en BenefitForm.Meta.model.
        queryset (QuerySet): El conjunto de datos utilizado para recuperar las instancias del beneficio.
        success_url (str): La URL a la que redirigir después de una eliminación exitosa.
        context_object_name (str): El nombre de la variable de contexto que contendrá el beneficio a eliminar.
    Métodos:
        get_context_data(self, **kwargs): Agrega datos adicionales al contexto de la vista.
        get(self, request: HttpRequest, slug=None, *args, **kwargs): Maneja las solicitudes GET para renderizar la página de confirmación de eliminación.
        form_valid(self, form): Maneja el envío exitoso del formulario, mostrando un mensaje de éxito.
    """
    template_name="benefit/delete.html"
    model=BenefitForm.Meta.model
    queryset=BenefitForm.Meta.model.objects.all()
    success_url=reverse_lazy('benefit_index')
    context_object_name="benefit"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Beneficios"
        return context
    
    def get(self, request:HttpRequest,slug=None, *args, **kwargs):
        benefit = self.model.objects.filter(slug=slug).first()
        if benefit :
            context ={
                'benefit':benefit
            }
            return render(request,self.template_name,context)
        messages.error(request,message="No Existe el Beneficio")
        return redirect(reverse_lazy("benefit_index"))
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El beneficio se ha eliminado correctamente")
        return super().form_valid(form)

class FoundProductsListView(ListView):
    template_name="benefit/search.html"
    model= BenefitForm.Meta.model
    queryset = model.objects.all().order_by('name')
    context_object_name="benefits"
    
    def get(self, request, *args, **kwargs):
        benefits=[]
        query = str(request.GET.get('query'))
        if query:
            benefits = self.model.objects.select_related().filter(
                Q(product__name__icontains=query)|
                Q(sku__icontains=query)|
                Q(bar_code__icontains=query)
            ).all()
        print(benefits)
        if benefits:
            context={
                "title":"Busqueda",
                "benefits_list":benefits
            }
            return render(request,self.template_name,context)
        context={
                "title":"Busqueda",
                "benefits_list":[]
            }
        messages.error(request,"No se econtro el producto buscado")
        return render(request,self.template_name,context)
    