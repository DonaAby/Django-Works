from django.shortcuts import render,redirect
from django.views.generic import View,FormView
from movie.forms import RegistrationForm,LoginForm,MovieForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from movie.models import Movie
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"login required")
            return redirect("signin")
        return fn(request,*args,**kwargs)
    return wrapper

class SignUpView(View):
    model=User
    template_name="register.html"
    form_class=RegistrationForm

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Registered")
            return redirect("signin")
        messages.error(request,"Not Registered")
        return render(request,self.template_name,{"form":form})
    
class SignInView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
        messages.error(request,"Invalid")
        return render(request,self.template_name,{"form":form}) 
    
@method_decorator(signin_required,name="dispatch")
class IndexView(View):
    template_name="index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name) 
    
@method_decorator(signin_required,name="dispatch")
class MovieCreateView(View):
    model=Movie
    form_class=MovieForm
    template_name="movie-add.html"
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"movie added successfully")
            return redirect("movie-list")
        messages.error(request,"failed to add movie")
        return render(request,self.template_name,{"form":form})
     
@method_decorator(signin_required,name="dispatch")
class MovieListView(View):
    model=Movie
    template_name="movie-list.html"
    def get(self,request,*args,**kwargs):
        qs=Movie.objects.filter(user=request.user).order_by("-created_date")
        return render(request,self.template_name,{"movie":qs})    

@method_decorator(signin_required,name="dispatch")
class MovieDetailView(View):
    model=Movie
    template_name="movie-detail.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Movie.objects.get(id=id)
        return render(request,self.template_name,{"movie":qs})   

@method_decorator(signin_required,name="dispatch")
class MovieEditView(View):
    model=Movie
    form_class=MovieForm
    template_name="movie-edit.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Movie.objects.get(id=id)
        form=self.form_class(instance=obj)
        return render(request,self.template_name,{"form":form})    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Movie.objects.get(id=id)
        form=self.form_class(instance=obj,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"movie updated")
            return redirect("movie-list")
        messages.error(request,"failed to update movie")
        return render(request,self.template_name,{"form":form}) 
    
@signin_required
def movie_delete_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    obj=Movie.objects.get(id=id)
    if obj.user==request.user:
        Movie.objects.get(id=id).delete()
        messages.success(request,"movie removed")
        return redirect("movie-list")
    else:
        messages.error(request,"you cannot perform this action")
        return redirect("signin")

def sign_out_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect("signin")
class PasswordResetView(FormView):
    model=User
    template_name="password-reset.html"
    form_class=PasswordResetForm
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")

            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"password has been changed")
                    return redirect("signin")
                except Exception as e:
                    messages.error(request,"Invalid credentials")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"password mismatch")
                return render(request,self.template_name,{"form":form})    






    

