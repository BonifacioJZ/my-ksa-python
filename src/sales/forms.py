from django import forms
from django.forms import Select,DateInput,DecimalField
from .models import Sale
from datetime import datetime
class SaleForm(forms.ModelForm):
    total = forms.DecimalField(disabled=True,max_digits=10,decimal_places=2,widget=forms.TextInput(
        attrs={
            "value":0.0
        }
    ))
    def __ini__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
    
    class Meta:
        model = Sale
        fields= ('date','client','status','total')
        widgets={
            'client': Select(attrs={
                'class':'form-control select2',
                'style':'width:100%'
            }),
            'date': DateInput(format='%d-%m-%Y',
                            attrs={
                                'class':'form-control datetimepicker-input"',
                                'value':datetime.now().strftime("%d-%m-%Y")
                            },
            )
        }
