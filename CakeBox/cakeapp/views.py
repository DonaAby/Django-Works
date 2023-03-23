from django.shortcuts import render,redirect
from django.views.generic import View
from django import forms
from cakeapp.models import Cakes
from django.contrib.auth.models import User


class CakeForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "flavour":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.TextInput(attrs={"class":"form-control"}),
            "shape":forms.TextInput(attrs={"class":"form-control"}),
            "weight":forms.TextInput(attrs={"class":"form-control"}),
            "layer":forms.TextInput(attrs={"class":"form-control"}),
            "number":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control","rows":5}),
            "picture":forms.FileInput(attrs={"class":"form-control"})
             }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),
        }

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})        
    
class CakeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request,"cake-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=CakeForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save() 
            return redirect("cake-list")
        return render(request,"cake-add.html",{"form":form})
    
class CakeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cakes.objects.all()
        return render(request,"cake-list.html",{"cake":qs})
    
class CakeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakes.objects.get(id=id)   
        return render(request,"cake-detail.html",{"cakes":qs})
    
class CakeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cakes.objects.get(id=id).delete()
        return redirect("cake-list")
    
class CakeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ck=Cakes.objects.get(id=id)
        form=CakeForm(instance=ck)
        return render(request,"cake-edit.html",{"form":form}) 
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ck=Cakes.objects.get(id=id)
        form=CakeForm(instance=ck,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cake-detail",pk=id)
        return render(request,"cake-edit.html",{"form":form})     
            
    
