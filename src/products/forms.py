from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit,Row,Column 
from tinymce.widgets import TinyMCE
from .models import Benefit,Brand,Product
from src.category.models import Category

class BrandForms(forms.ModelForm):
    name = forms.CharField(max_length=150,required=True,label="Nombre")
    
    class Meta:
        ordering = ['name']
        model = Brand
        fields = ["name",]
        
##Crear Fourmulario
class ProductForms(forms.ModelForm):
    name = forms.CharField(max_length=150,required=True,label="Nombre")
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 20}),required=False,label="Descripcion")
    new_category = forms.CharField(
        required=False,
        label="Nueva Categoria",
        help_text="Si no encuentra la categoria que busca, por favor ingrese una nueva"
    )
    image = forms.ImageField(required=False,label="Foto")
    
    class Meta:
        model = Product
        fields = ["name","brand","category","image","description"]
        widgets = {
            "description": TinyMCE(attrs={"cols": 80, "rows": 20}),
        }
        
    def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("brand", css_class="col-md-6"),
                css_class="row"
            ),
            "descripcion",
            Row(
                Column("category", css_class="col-md-6"),
                Column("new_category", css_class="col-md-6"),
                css_class="row"
            ),
            Submit("submit", "Guardar ", css_class="btn btn-primary")
        )
    def clean(self):
            cleaned_data = super().clean()
            new_category = cleaned_data.get('new_category')
            if new_category:
                category,created = Category.objects.get_or_create(name=new_category)
                cleaned_data['category'] = category
            return cleaned_data