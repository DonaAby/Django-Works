from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import View, CreateView,FormView,TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from myapp.forms import SignUpForm,LoginForm

class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name="register.html"
    success_url=reverse_lazy("login")

    def form_valid(self, form): 
        messages.success(self.request,"Account has been created!!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"failed to create account!!")
        return super().form_invalid(form)

class SignInView(FormView):
    
    template_name="login.html"
    form_class=LoginForm 
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)   
            if usr:                                         
                login(request,usr)
                messages.success(request,"logged in successfully")
                return redirect("index")
        messages.error(request,"Invalid")
        return render(request,self.template_name,{"form":form}) 

class IndexView(TemplateView):
    template_name="index.html"
    success_url=reverse_lazy("index")     
    
     

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("login")    
