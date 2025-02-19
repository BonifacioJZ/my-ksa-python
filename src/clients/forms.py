from django import forms
from .models import Client

class ClientForms(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','last_name','email','phone','address']
        