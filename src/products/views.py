from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BrandForms,ProductForms,BenefitForm
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
    template_name="brand/form.html"
    model=BrandForms.Meta.model
    form_class= BrandForms
    queryset = BrandForms.Meta.model.objects.all()
    success_url=reverse_lazy('brand_index')
    
    
    def get_context_data(self, **kwargs) :
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
    template_name="product/index.html"
    model=ProductForms.Meta.model
    queryset=ProductForms.Meta.model.objects.all().select_related().order_by('name')
    context_object_name="products_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos" 
        return context
    
class ProductCreateView(LoginRequiredMixin,CreateView):
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
        messages.success(request=self.request,message="El producto se a guardado correctamente")
        return super().form_valid(form)

class ProductDetailView(LoginRequiredMixin,DetailView):
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
        messages.success(request=self.request,message="El producto se a actualizado correctamente")
        return super().form_valid(form)
    
class ProductDeleteView(LoginRequiredMixin,DeleteView):
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
        messages.success(request=self.request,message="El producto se a eliminado correctamente")
        return super().form_valid(form)
    
class BenefitListView(LoginRequiredMixin,ListView):
    template_name="benefit/index.html"
    model=BenefitForm.Meta.model
    queryset=BenefitForm.Meta.model.objects.all().order_by('name')
    context_object_name="benefits_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Beneficios" 
        return context

class BenefitCreateView(LoginRequiredMixin,CreateView):
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
        messages.success(request=self.request,message="El beneficio se a guardado correctamente")
        return super().form_valid(form)

class BenefitUpdateView(LoginRequiredMixin,UpdateView):
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
        messages.success(request=self.request,message="El beneficio se a actualizado correctamente")
        return super().form_valid(form)

class BenefitDeleteView(LoginRequiredMixin,DeleteView):
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
        messages.success(request=self.request,message="El beneficio se a eliminado correctamente")
        return super().form_valid(form)