from django.shortcuts import render,redirect
from django.views.generic import View
from django import forms
from cakeapp.models import Cakes
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


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

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),
        }
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class SignUpView(View): #register
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered successfully")
            return redirect("signin")
        messages.error(request,"Error")
        return render(request,"register.html",{"form":form})   

class SignInView(View): #sign in 
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"logged in")
                return redirect("cake-list")
        messages.error(request,"Error")    
        return render(request,"login.html",{"form":form})            
    
class CakeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request,"cake-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=CakeForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request,"Created successfully")
            return redirect("cake-list")
        messages.error(request,"not created")
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
        messages.success(request,"removed successfully")
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
            messages.success(request,"edited successfully")
            return redirect("cake-detail",pk=id)
        messages.error(request,"not updated")
        return render(request,"cake-edit.html",{"form":form})     

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")     
            
    
