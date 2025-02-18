from django.db import models
import uuid
from django.db.models.signals import pre_save
from django.utils.text import slugify
from src.clients.models import Client
from src.products.models import Benefit
# Create your models here.

class Sale(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name="Total",max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
    
    def __str__(self) -> str:
        return self.client.name

class Detail(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE)
    product = models.ForeignKey(Benefit,verbose_name="Producto",related_name="product",on_delete=models.CASCADE)
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
        return self.product
