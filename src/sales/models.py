import string
from django.db import models
import uuid
import random
from datetime import datetime
from django.db.models.signals import pre_save
from django.utils.text import slugify
from src.clients.models import Client
from src.products.models import Benefit
# Create your models here.

class Sale(models.Model):
    CHOICES =[
        ('paid','Pagado'),
        ('pending','Pendiente'),
        ('canceled','Cancelado')
        ]
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    folio = models.CharField(max_length=20,unique=True,blank=True)
    client = models.ForeignKey(Client,verbose_name="Cliente",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)  
    total = models.DecimalField(verbose_name="Total",max_digits=10,decimal_places=2)
    pay = models.DecimalField(verbose_name="Pago",max_digits=10,decimal_places=2,blank=True,null=True)
    change = models.DecimalField(verbose_name="Cambio",max_digits=10,decimal_places=2,blank=True,null=True)
    status = models.CharField(choices=CHOICES,max_length=15,verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
    
    def __str__(self) -> str:
        return f"{self.client.name} - {self.client.last_name} - {self.folio}"
    
    def save(self, *args, **kwargs):
        if not self.folio:
            date = datetime.now().strftime("%Y%m%d")
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.folio = f"{date}-{rand}"  # Formato 20240219-ABC12
        super().save(*args, **kwargs)

class Detail(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    sale = models.ForeignKey(Sale,verbose_name="Venta",related_name="sales",on_delete=models.CASCADE)
    product = models.ForeignKey(Benefit,verbose_name="Producto",related_name="products",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Cantidad",blank=False,null=False)
    price = models.DecimalField(verbose_name="Precio",max_digits=10,decimal_places=2)
    total = models.DecimalField(verbose_name="Total",max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        verbose_name = 'detail'
        verbose_name_plural = 'details'
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.product.product.name} - {self.sale.folio}"
