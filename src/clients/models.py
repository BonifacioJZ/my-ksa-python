from django.db import models
import uuid
from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.

class Client(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(verbose_name="Nombre",max_length=150,blank=False,null=False)
    last_name = models.CharField(verbose_name="Apellido",max_length=150,blank=False,null=False)
    email = models.EmailField(verbose_name="Correo Electronico",max_length=254,blank=True,null=True)
    phone = models.CharField(verbose_name="Telefono",max_length=15,blank=False,null=False)
    address = models.TextField(verbose_name="Direccion",null=True, blank=True)
    slug = models.SlugField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        verbose_name = 'client'
        verbose_name_plural = 'clients'
    
    def __str__(self) -> str:
        return f"{self.name} {self.last_name} {self.slug}"
    

def create_client_slug(sender,instance:Client,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))

pre_save.connect(create_client_slug,sender=Client)