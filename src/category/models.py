import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(verbose_name="Nombre",max_length=150,blank=False,null=False)
    description = models.TextField(verbose_name="Descripcion",null=True, blank=True)
    slug = models.SlugField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self) -> str:
        return self.name
    
    


def create_category_slug(sender,instance:Category,*args, **kwargs):
    if instance.slug:
        return
    
    id = str(uuid.uuid4())
    instance.slug = slugify('{}-{}'.format(
        instance.name.upper().strip(),id[:8]
    ))


pre_save.connect(create_category_slug,sender=Category)