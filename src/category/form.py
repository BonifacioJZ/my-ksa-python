from django import forms
from .models import Category


class CategoryForms(forms.ModelForm):
    name = forms.CharField(max_length=150,required=True,label='Nombre')
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":2,"col":40}))
    class Meta:
        model = Category
        fields = ['name','description',]