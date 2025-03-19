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
from .views import SalesCreateView,add_product,remove_product,add_one_product,subtract_one_product
from django.urls import path

urlpatterns = [
    path('',SalesCreateView.as_view(),name="sales_index"),
    path('add/<str:slug>/',add_product,name="add_product"),
    path('add_one/<str:pk>/',add_one_product,name="add_one_product"),
    path('subtract_one/<str:pk>/',subtract_one_product,name="remove_one_product"),
    path('remove/<str:pk>/',remove_product,name="remove_product"),
    
]
