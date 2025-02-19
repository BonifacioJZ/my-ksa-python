from django.db import models
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nombre")
    address = models.TextField(verbose_name="Direccion")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name="Telefono")
    email = models.EmailField(null=True, blank=True,verbose_name="Correo Electronico")
    whatsapp = models.CharField(max_length=13, null=True, blank=True, verbose_name="Whatsapp")
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
    def __str__(self):
        return self.name

class SupplierContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier,verbose_name="Provedor", related_name="suppler", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellido", null=False, blank=False)
    phone = models.CharField(max_length=15,verbose_name="Telefono")
    email = models.EmailField(null=True, blank=True,verbose_name="Correo Electronico")
    whatsapp = models.CharField(max_length=13, null=True, blank=True, verbose_name="Whatsapp")
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Supplier Contact"
        verbose_name_plural = "Supplier Contacts"
    def __str__(self):
        return self.name
    
    

def create_supplier_slug(sender,instance:Supplier,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))
def create_supplier_contact_slug(sender,instance:SupplierContact,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))
pre_save.connect(create_supplier_slug,sender=Supplier)
pre_save.connect(create_supplier_contact_slug,sender=SupplierContact)