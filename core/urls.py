"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from src.products.urls import urlpatterns_benefit as benefit_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/',include('src.user.urls')),
    path('category/',include('src.category.urls')),
    path('product/',include('src.products.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('products/benefit/',include(benefit_urls)),
    path('supplier/',include('src.suppliers.urls')),
    path('clients/',include('src.clients.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
