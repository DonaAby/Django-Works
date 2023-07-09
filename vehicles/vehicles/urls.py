"""
URL configuration for vehicles project.

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
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehicle/add/',views.VehicleCreateView.as_view(),name="add"),
    path('vehicle/all/',views.VehicleListView.as_view(),name="list"),
    path('vehicle/detail/<int:pk>/',views.VehicleDetailView.as_view(),name="detail"),
    path('vehicle/edit/<int:pk>/',views.VehicleEditView.as_view(),name="edit"),
    path('vehicle/delete/<int:pk>/',views.VehicleDeleteView.as_view(),name="delete")
]
