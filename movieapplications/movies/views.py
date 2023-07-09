from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,CreateView,ListView,DetailView,UpdateView
from movies.forms import RegistrationForm,LoginForm,MovieForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from movies.models import Movie
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"login required")
            return redirect("signin")
        return fn(request,*args,**kwargs)
    return wrapper

class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"Successfully Registered")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,"Not registered")
        return super().form_invalid(form)

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"Successfully Registered")
    #         return redirect("signin")
    #     messages.error(request,"Not Registered")
    #     return render(request,self.template_name,{"form":form})

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
class IndexView(TemplateView):
    
    template_name="index.html"
    # def get(self,request,*args,**kwargs):
    #     return render(request,self.template_name) 
    
@method_decorator(signin_required,name="dispatch")
class MovieCreateView(CreateView):
    model=Movie
    form_class=MovieForm
    template_name="movies-add.html"
    success_url=reverse_lazy("movies-list")
    def form_valid(self, form):
        messages.success(self.request,"movie added successfully")
        return super().form_valid(form)
    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(data=request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"movie added successfully")
    #         return redirect("movies-list")
    #     messages.error(request,"failed to add movie")
    #     return render(request,self.template_name,{"form":form})
     
@method_decorator(signin_required,name="dispatch")
class MovieListView(ListView):
    model=Movie
    template_name="movies-list.html"
    context_object_name="movies"
    def get_queryset(self):

        return Movie.objects.all()
    # def get(self,request,*args,**kwargs):
    #     qs=Movie.objects.all()
    #     return render(request,self.template_name,{"movies":qs})    

@method_decorator(signin_required,name="dispatch")
class MovieDetailView(DetailView):
    model=Movie
    template_name="movies-detail.html"
    context_object_name="movies"
    # def get(self,request,*args,**kwargs):
        # id=kwargs.get("pk")
        # qs=Movie.objects.get(id=id)
        # return render(request,self.template_name,{"movies":qs})   

@method_decorator(signin_required,name="dispatch")
class MovieEditView(UpdateView):
    model=Movie
    form_class=MovieForm
    template_name="movies-edit.html"
    success_url=reverse_lazy("movies-list")
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Movie.objects.get(id=id)
    #     form=self.form_class(instance=obj)
    #     return render(request,self.template_name,{"form":form})    
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Movie.objects.get(id=id)
    #     form=self.form_class(instance=obj,data=request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"movie updated")
    #         return redirect("movies-list")
    #     messages.error(request,"failed to update movie")
    #     return render(request,self.template_name,{"form":form}) 
    
@signin_required
def movie_delete_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    Movie.objects.get(id=id).delete()
    return redirect('movies-list')
    

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




