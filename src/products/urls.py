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
from .views import BrandListView,BrandCreateView,BrandDetailView,BrandUpdateView,BrandDeleteView
from .views import ProductListView,ProductCreateView,ProductDetailView,ProductUpdateView,ProductDeleteView
from django.urls import path

urlpatterns = [
    path('',ProductListView.as_view(),name="product_index"),
    path('brand/',BrandListView.as_view(),name="brand_index"),
    path('new/',ProductCreateView.as_view(),name="product_store"),
    path('<str:slug>/',ProductDetailView.as_view(),name="product_detail"),
    path('<str:slug>/edit/',ProductUpdateView.as_view(),name="product_edit"),
    path('<str:slug>/delete/',ProductDeleteView.as_view(),name="product_delete"),
    path('brand/new/',BrandCreateView.as_view(),name="brand_store"),
    path('brand/<str:slug>/',BrandDetailView.as_view(),name="brand_detail"),
    path('brand/<str:slug>/edit/',BrandUpdateView.as_view(),name="brand_edit"),
    path('brand/<str:slug>/delete/',BrandDeleteView.as_view(),name="brand_delete")
]
