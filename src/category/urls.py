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
from .views import CategoryListView,CategoryCreateView,CategoryDetailView,CategoryUpdateView,DeleteCategoryView
from django.urls import path

urlpatterns = [
    path('',CategoryListView.as_view(),name="category_index" ),
    path('new/',CategoryCreateView.as_view(),name="category_store"),
    path('<str:slug>/',CategoryDetailView.as_view(),name="category_show"),
    path('<str:slug>/edit/',CategoryUpdateView.as_view(),name="category_edit"),
    path('<str:slug>/delete/',DeleteCategoryView.as_view(),name="category_delete"),
    
]
