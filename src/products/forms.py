from django import forms
from .models import Benefit,Brand,Product

class BrandForms(forms.ModelForm):
    name = forms.CharField(max_length=150,required=True,label="Nombre")
    
    class Meta:
        ordering = ['name']
        model = Brand
        fields = ["name",]
        
##Crear Fourmulario
class ProductForms(forms.ModelForm):
    pass