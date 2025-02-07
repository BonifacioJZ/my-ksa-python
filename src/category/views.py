from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from .form import CategoryForms
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,render


class CategoryListView(LoginRequiredMixin,ListView):
    template_name="category/index.html"
    paginate_by=20
    model = CategoryForms.Meta.model
    context_object_name='category_list'
    queryset = CategoryForms.Meta.model.objects.all().order_by('name').values()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Categorias' 
        return context

class CategoryCreateView(LoginRequiredMixin,CreateView):
    template_name = "category/form.html"
    model= CategoryForms.Meta.model
    form_class = CategoryForms
    queryset = CategoryForms.Meta.model.objects.all()
    success_url = reverse_lazy('category_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categorias" 
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        form = CategoryForms(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message="La categoria fue creada exitosamente")
            return redirect(self.success_url)
        context = {
            'form':form
        }
        return render(request,self.template_name,context=context)

class CategoryDetailView(LoginRequiredMixin,DetailView):
    model=CategoryForms.Meta.model
    template_name="category/show.html"
    queryset = CategoryForms.Meta.model.objects.all()
    context_object_name = "Categorias"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categorias" 
        return context
    
    def get(self, request: HttpRequest, slug=None,*args, **kwargs) -> HttpResponse:
        category = CategoryForms.Meta.model.objects.filter(slug=slug).first()
        if category:
            context = {
                'category':category
            }
            return render(request,self.template_name,context=context)
        messages.error(request,message="No Existe la categoria")
        return redirect(reverse_lazy("category_index"))

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "category/form.html"
    model=CategoryForms.Meta.model
    form_class=CategoryForms
    queryset=CategoryForms.Meta.model.objects.all()
    success_url = reverse_lazy('category_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categorias" 
        return context
    
    def form_valid(self, form):
        messages.success(self.request,message="La categoria fue actualizada exitosamente")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,message="Error al Actualizar")
        response = super().form_invalid(form)
        return response
    
    
    
    
    
class DeleteCategoryView(LoginRequiredMixin,DeleteView):
    template_name="category/delete.html"
    model=CategoryForms.Meta.model
    success_url=reverse_lazy('category_index')
    context_object_name="category"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category" 
        return context
    
    def get(self, request: HttpRequest,slug=None, *args, **kwargs) -> HttpResponse:
        category = CategoryForms.Meta.model.objects.filter(slug=slug).first()
        if category:
            context = {
                'category':category
            }
            return render(request,self.template_name,context=context)
        messages.error(request,message="No Existe la categoria")
        return redirect(reverse_lazy("category_index"))
            
    
    def form_valid(self, form):
        messages.success(request=self.request,message="La categoria se a eliminado correctamente")
        return super().form_valid(form)
    
    
    