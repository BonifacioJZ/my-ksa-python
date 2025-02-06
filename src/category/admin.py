from django.contrib import admin
from django.db import models
from .models import Category
from tinymce.widgets import TinyMCE
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
admin.site.register(Category,ProjectAdmin)