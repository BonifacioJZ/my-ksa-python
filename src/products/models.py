from django.db import models
import uuid
from src.category.models import Category
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.

class Brand(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(verbose_name="Marca",max_length=250,blank=False,null=False)
    slug = models.SlugField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(verbose_name="Nombre",max_length=250,blank=False,null=False)
    description = models.TextField(verbose_name="Descripcion",null=True,blank=True)
    image = models.ImageField( verbose_name="Foto",null=True,blank=True)
    category = models.ForeignKey(Category,verbose_name="Categoria",related_name="category",on_delete=models.CASCADE)
    slug = models.SlugField(null=True,blank=True)
    brand = models.ForeignKey(Brand,verbose_name="Marca",related_name="brand",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class Benefit(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(verbose_name="Nombre",max_length=250,blank=False,null=False)
    sku= models.CharField(verbose_name="SKU", unique=True,max_length=8,blank=False,null=False)
    bar_code= models.CharField(verbose_name="Codigo de Barras",max_length=13,blank=False,null=False)
    stock = models.IntegerField(verbose_name="Stock")
    price = models.DecimalField(verbose_name="Precio",max_digits=10,decimal_places=2,blank=False,null=False)
    product = models.ForeignKey(Product,verbose_name="Productos",related_name="products",on_delete=models.CASCADE)
    slug = models.SlugField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        verbose_name = "benefit"
        verbose_name_plural = "benefits"

    def __str__(self):
        return self.name


def create_brand_slug(sender,instance:Brand,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))


def create_product_slug(sender,instance:Product,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))

def create_benefit_slug(sender,instance:Benefit,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))
pre_save.connect(create_benefit_slug,sender=Benefit)
pre_save.connect(create_product_slug,sender=Product)
pre_save.connect(create_brand_slug,sender=Brand)
