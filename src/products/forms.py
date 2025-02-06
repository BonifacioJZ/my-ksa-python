from django import forms
from .models import Benefit,Brand,Product

class BrandForms(forms.Form):
    name = forms.CharField(max_length=150,required=True,label="Nombre")
    
    class Meta:
        model = Brand
        fields = ["name",]