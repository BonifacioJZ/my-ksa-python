from django import forms
from .models import Supplier,SupplierContact

class SupplierForm(forms.ModelForm):
    address = forms.CharField(label="Dirección",widget=forms.Textarea(attrs={"rows":3}))
    class Meta:
        model = Supplier
        fields = ["name","address","phone","email","whatsapp"]

class SupplierContactForm(forms.ModelForm):
    class Meta:
        model = SupplierContact
        fields = ["name","supplier","phone","email","whatsapp"]