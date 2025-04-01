from django import forms
from django.forms import Select,DateInput,DecimalField,CharField,TextInput
from .models import Sale
from datetime import datetime

class SearchProductForm(forms.Form):
    query = CharField(max_length=250,required=False,label="",widget=TextInput(attrs={
        "placeholder":"Ponga el Nombre o la Clave del producto",
        "class":"form-control",
    }))
class SaleForm(forms.ModelForm):
    total = DecimalField(required=False,max_digits=10,decimal_places=2,widget=TextInput(
        attrs={
            "readonly":True,
            "class":"form-control",
            "value":0.0

        }
    ))
    date = forms.DateField(required=False,widget=DateInput(attrs={
                                "readonly":True,
                                'class':'form-control datetimepicker-input"',
                                'value':datetime.now().strftime("%d-%m-%Y"),
                            }
    ))
    
    class Meta:
        model = Sale
        fields= ['client','status','total',]
        widgets={
            'client': Select(attrs={
                'class':'form-control select2',
                'style':'width:100%'
            }),
            'status':Select(attrs={
                'class':'form-control select2',
                'style':'width:100%',
            })
        }
    
        
