from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BrandForms
from .models import Product
from django.urls import reverse_lazy
# Create your views here.

#Zona de vistas para Brand
class BrandListView(LoginRequiredMixin,ListView):
    template_name="brand/index.html"
    paginate_by=20
    model = BrandForms.Meta.model
    context_object_name="brand_list"
    queryset=BrandForms.Meta.model.objects.all().order_by('name')
    
    
    def get_context_data(self, **kwargs):
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
        brand = self.queryset.filter(slug=slug).first()
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
    paginate_by=20
    model=Product
    queryset=Product.objects.all().order_by("name")
    context_object_name="products_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos" 
        return context
    
    