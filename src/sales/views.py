from django.shortcuts import redirect,render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView,DetailView,ListView,UpdateView
from .forms import SaleForm,SearchProductForm
from src.class_lib.Cart import Cart
from .context_process import total_cart
from src.clients.models import Client
from src.products.models import Benefit
from .models import Detail
from datetime import datetime
from src.class_lib import generators_pdf
# Create your views here.

class SalesIndexView(LoginRequiredMixin,TemplateView):
    template_name="sales/index.html"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Ventas"
        context["form"] = SaleForm()
        context["search"] = SearchProductForm()
        context["date"] = datetime.now().strftime("%d-%m-%Y")
        return context

class SalesCreateView(LoginRequiredMixin,CreateView):
    template_name="sales/form.html"
    form_class = SaleForm
    success_url = reverse_lazy('sales_index')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Ventas"
        context["subtitle"] = "Resumen de la venta"
        client_id = self.request.GET.get('client')
        context["client"] = Client.objects.filter(id=client_id).first()
        context["date"] = datetime.now().strftime("%d-%m-%Y")
        return context
    
    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart',{})
        
        sale:SaleForm.Meta.model = {} 
        if not cart:
            messages.error(request,"No hay productos en el carrito")
            return redirect(reverse_lazy('sales_index'))
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.total = total_cart(request)['total_cart']
            sale.client = Client.objects.filter(id=str(request.POST.get('client'))).first()
            sale.save()
            for item in cart.values():
                product = Benefit.objects.filter(id=item['id']).first()
                product.stock -= float(item['qty'])
                product.save()
                Detail.objects.create(
                    sale=sale,
                    product=product,
                    quantity=item['qty'],
                    price=item['price'],
                    total=item['total']
                )
            cart = Cart(request)
            cart.clear()
            messages.success(request,"Venta guardada correctamente")
            return redirect('sale_detail',sale.id)
        
        messages.error(request,"Error al guardar la venta")
        context ={
            "title": "Ventas",
            "form": form,
            "client": Client.objects.filter(id=str(request.POST.get('client'))).first(),
            "date": datetime.now().strftime("%d-%m-%Y"),
        }
        return render(request,self.template_name,context)
class SalesListView(LoginRequiredMixin,ListView):
    template_name="sales/list.html"
    model = SaleForm.Meta.model
    context_object_name = "sales"
    queryset = SaleForm.Meta.model.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Ventas"
        context["date"] = datetime.now().strftime("%d-%m-%Y")
        return context
    
class SaleDetailView(LoginRequiredMixin,DetailView):
    template_name="sales/show.html"
    model = SaleForm.Meta.model
    context_object_name = "sale"
    queryset = SaleForm.Meta.model.objects.all()
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Ventas"
        return context
    
    def get(self, request,pk=None, *args, **kwargs):
        sale:SaleForm.Meta.model = self.get_queryset().prefetch_related().filter(id=pk).first()
        
        if sale:
            context= {
            "title": "Ventas",
            "sale":sale,
            "date": datetime.now().strftime("%d-%m-%Y"),
            "user": request.user.username,
            "details": sale.sales.all(),
            "client": sale.client,
        }
            
            return render(request,self.template_name,context)
        else:
            messages.error(request,"No se encontro la venta")
            return redirect(reverse_lazy('sales_index'))

class SalesUpdateView(LoginRequiredMixin,UpdateView):
    template_name="sales/edit.html"
    model = SaleForm.Meta.model
    form_class = SaleForm
    context_object_name = "sale"
    queryset = SaleForm.Meta.model.objects.prefetch_related().all()
    success_url = reverse_lazy('sales_list')
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Ventas"
        context["subtitle"] ="Editar ventas"
    
    def get(self, request, folio=None, *args, **kwargs):
        sale=SaleForm.Meta.model = self.get_queryset().prefetch_related().filter(folio=folio).first()
        if sale:
            context = {
                "title": "Ventas",
                "sale": sale,
                "form": self.get_form(),
                "date": datetime.now().strftime("%d-%m-%Y"),
                "details": sale.sales.all(),
                "client": sale.client,
            }
            return render(request,self.template_name,context) 
        return super().get(request, *args, **kwargs)

def generate_ticket(request:HttpRequest,folio=None):
    sale= SaleForm.Meta.model.objects.prefetch_related().filter(folio=folio).first()
    context = {
        "folio":folio,
        "sale":sale,
        "title":"Ticket",
        "date":datetime.now().strftime("%d-%m-%Y"),
        "logo_path": request.build_absolute_uri('/static/img/log.png'),
        "cart":sale.sales.all(),
        "total":sale.total,
    }
    return generators_pdf.ticket_generator(request,'tickets/ticket.html',context)
def generate_pdf(request:HttpRequest,folio=None):
    sale= SaleForm.Meta.model.objects.prefetch_related().filter(folio=folio).first()
    context = {
        "client":sale.client,
        "sale":sale,
        "title":"Factura",
        "user":request.user.username,
        "date":datetime.now().strftime("%d-%m-%Y"),
        "cart":sale.sales.all(),
        "total":sale.total,
    }
    return generators_pdf.generators_pdf(request,'pdf/factura.html',context)

def add_product(request:HttpRequest,slug:str):
    cart = Cart(request)
    if request.POST:
        product = Benefit.objects.select_related().filter(slug=slug).first()
        qty = float(request.POST.get('qty'))
        success = cart.add(product,qty)
        if not success:
            messages.error(request,"No hay suficiente stock")
            return render(request,'components/_close_windows.html')
        messages.success(request,"Producto agregado al carrito")
        return render(request,'components/_close_windows.html')

def add_one_product(request:HttpRequest,pk:str):
    cart = Cart(request)
    product = Benefit.objects.select_related().filter(id=pk).first()
    success = cart.add(product,1)
    if not success:
        messages.error(request,"No hay suficiente stock")
        return redirect(reverse_lazy('sales_index'))
    messages.success(request,"Producto agregado al carrito")
    return redirect(reverse_lazy('sales_index'))

def subtract_one_product(request:HttpRequest,pk:str):
    cart = Cart(request)
    product = Benefit.objects.select_related().filter(id=pk).first()
    success = cart.subtract(product,1)
    if not success:
        messages.error(request,"No se encuentra el producto en el carrito")
        return redirect('sales_index')
    messages.success(request,"Se eliminado un elemento  del carrito")
    return redirect('sales_index')
    

def remove_product(request:HttpRequest,pk:str):
    cart = Cart(request)
    product = Benefit.objects.select_related().filter(id=pk).first()
    cart.remove(product)
    messages.success(request,"Producto eliminado del carrito")
    return redirect('sales_index')
    