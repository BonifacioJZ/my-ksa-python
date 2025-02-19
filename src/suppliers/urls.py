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
from .views import SupplierListView,SupplierCreateView,SupplierDetailView,SupplierUpdateView,SupplierDeleteView
from .views import SupplierContactListView,SupplierContactCreateView,SupplierContactDetailView,SupplierContactUpdateView,SupplierContactDeleteView
from django.urls import path

urlpatterns = [
    path('',SupplierListView.as_view(),name="supplier_index" ),
    path('contacts/',SupplierContactListView.as_view(),name="supplier_contact_index" ),
    path('new/',SupplierCreateView.as_view(),name="supplier_store" ),
    path('new/contact/',SupplierContactCreateView.as_view(),name="supplier_contact_store" ),
    path('<str:slug>/',SupplierDetailView.as_view(),name="supplier_detail" ),
    path('<str:slug>/contact/',SupplierContactDetailView.as_view(),name="supplier_contact_detail" ),
    path('<str:slug>/edit/',SupplierUpdateView.as_view(),name="supplier_edit" ),
    path('<str:slug>/edit/contact/',SupplierContactUpdateView.as_view(),name="supplier_contact_edit" ),
    path('<str:slug>/delete/contact/',SupplierContactDeleteView.as_view(),name="supplier_contact_delete" ),
    path('<str:slug>/delete/',SupplierDeleteView.as_view(),name="supplier_delete" ),
]
