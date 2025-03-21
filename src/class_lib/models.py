import uuid,datetime
from django.db import models
# Create your models here.
class Person(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    first_name = models.CharField(verbose_name="Nombre",max_length=255,null=False,blank=False)
    last_name = models.CharField(verbose_name="Apellidos",max_length=255,null=False,blank=False)
    phone = models.CharField(verbose_name="Telefono",max_length=13,null=True,blank=True,default="000-000-0000")
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract =True