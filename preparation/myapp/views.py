from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,ListView,DetailView,UpdateView
from myapp.models import Vehicle
from myapp.forms import VehicleForm

class VehicleCreateView(CreateView):
    form_class=VehicleForm
    template_name="vehicle-add.html"
    model=Vehicle
    success_url=reverse_lazy("add")

class VehicleListView(ListView):
    model=Vehicle
    template_name="vehicle-list.html"
    context_object_name="vehicles"

class VehicleDetailView(DetailView):
    model=Vehicle
    template_name="vehicle-detail.html"
    context_object_name="vehicle"

class VehicleEditView(UpdateView):
    model=Vehicle
    form_class=VehicleForm
    template_name="vehicle-edit.html"
    success_url=reverse_lazy("list")

class VehicleDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Vehicle.objects.get(id=id).delete()
        return redirect("list")
