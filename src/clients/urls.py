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
from .views import ClientListView,ClientCreateView,ClientDetailView,ClientUpdateView,ClientDeleteView,ClientCreateViewEmergent
from django.urls import path

urlpatterns = [
    path('',ClientListView.as_view(),name='client_index'),
    path('new/',ClientCreateView.as_view(),name='client_store'),
    path('<str:slug>/',ClientDetailView.as_view(),name="client_detail"),
    path('<str:slug>/edit/',ClientUpdateView.as_view(),name="client_edit"),
    path('<str:slug>/delete/',ClientDeleteView.as_view(),name="client_delete"),
    path('new/emergent/',ClientCreateViewEmergent.as_view(),name="client_store_emergent"),
]
