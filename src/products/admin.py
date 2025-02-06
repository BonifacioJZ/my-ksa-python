from django.contrib import admin
from django.db import models
from .models import Brand,Benefit,Product
from tinymce.widgets import TinyMCE

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
admin.site.register(Brand)
admin.site.register(Benefit)
admin.site.register(Product,ProjectAdmin)