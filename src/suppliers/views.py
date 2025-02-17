from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from .forms import SupplierForm,SupplierContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
class SupplierListView(LoginRequiredMixin,ListView):
    template_name = "supplier/index.html"
    model = SupplierForm.Meta.model
    context_object_name = 'suppliers_list'
    queryset = SupplierForm.Meta.model.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context

class SupplierCreateView(LoginRequiredMixin,CreateView):
    template_name = "supplier/form.html"
    model = SupplierForm.Meta.model
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context
    
    def post(self, request:HttpRequest, *args, **kwargs):
        form = SupplierForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message="El Proveedor  fue creado exitosamente")
            return redirect(self.success_url)
        context ={
            'form':form
        }
        messages.error(request=request,message="Error al crear el Proveedor")
        return render(request,self.template_name,context)
    
class SupplierDetailView(LoginRequiredMixin,DetailView):
    template_name = "supplier/show.html"
    model = SupplierForm.Meta.model
    context_object_name = 'supplier'
    queryset = SupplierForm.Meta.model.objects.all()
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedor" 
        return context
    
    def get(self, request,slug=None, *args, **kwargs):
        supplier = self.queryset.select_related().all().filter(slug=slug).first()
        if supplier:
            return render(request,self.template_name,{'supplier':supplier})
        messages.error(request,message="No Existe el Producto")
        return redirect(reverse_lazy("product_index"))

class SupplierUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "supplier/form.html"
    model = SupplierForm.Meta.model
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context
    
    def post(self, request:HttpRequest, *args, **kwargs):
        supplier = self.get_object()
        form = SupplierForm(instance=supplier,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message="El Proveedor  fue actualizado exitosamente")
            return redirect(self.success_url)
        context ={
            'form':form
        }
        messages.error(request=request,message="Error al actualizar el Proveedor")
        return render(request,self.template_name,context)

class SupplierDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "supplier/delete.html"
    model = SupplierForm.Meta.model
    success_url = reverse_lazy('supplier_index')
    context_object_name = "supplier"
    
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Proveedores" 
        return context
    
    def get(self, request:HttpRequest,slug=None, *args, **kwargs):
        supplier = self.model.objects.filter(slug=slug).first()
        if supplier :
            context ={
                'supplier':supplier
            }
            return render(request,self.template_name,context)
        messages.error(request,message="No Existe el Proveedor")
        return redirect(reverse_lazy("supplier_index"))
    
    def form_valid(self, form):
        messages.success(request=self.request,message="El Proveedor se a eliminado correctamente")
        return super().form_valid(form)