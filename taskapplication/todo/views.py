from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,ListView,DetailView,UpdateView,CreateView
from todo.forms import RegistrationForm,LoginForm,TaskForm,TaskChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from todo.models import Task
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

#decorator

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
    
#template inheritance
@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    #render index.html
    template_name="index.html"
    # def get(self,request,*args,**kwargs):
    #     return render(request,self.template_name)   

#localhost:8000/todos/add/
@method_decorator(signin_required,name="dispatch")
class TaskCreateView(CreateView):
    model=Task
    form_class=TaskForm
    template_name="task-add.html"
    success_url=reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo created")
        return super().form_valid(form)
    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
            
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(request,"todo added successfully")
    #         return redirect("task-list")
    #     messages.error(request,"failed to create todo")
    #     return render(request,self.template_name,{"form":form}) 
    
@method_decorator(signin_required,name="dispatch")    
class TaskListView(ListView):
    model=Task
    template_name="task-list.html"
    context_object_name="tasks"
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_date") 
    # def get(self,request,*args,**kwargs):
    #     qs=Task.objects.filter(user=request.user).order_by("-created_date")
    #     return render(request,self.template_name,{"tasks":qs})    

@method_decorator(signin_required,name="dispatch")
class TaskDetailView(DetailView):
    model=Task
    template_name="task-detail.html"
    context_object_name="task"
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Task.objects.get(id=id)
    #     return render(request,self.template_name,{"task":qs})

@method_decorator(signin_required,name="dispatch")
class TaskEditView(UpdateView):
    model=Task
    form_class=TaskChangeForm
    template_name="task-edit.html"
    success_url=reverse_lazy("task-list")
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Task.objects.get(id=id)
    #     form=self.form_class(instance=obj)
    #     return render(request,self.template_name,{"form":form})    
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Task.objects.get(id=id)
    #     form=self.form_class(instance=obj,data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"todo changed")
    #         return redirect("task-list")
    #     messages.error(request,"failed to update todo")
    #     return render(request,self.template_name,{"form":form})

@signin_required
def task_delete_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    obj=Task.objects.get(id=id)
    if obj.user==request.user:
        Task.objects.get(id=id).delete()
        messages.success(request,"task removed")
        return redirect("task-list")
    else:
        messages.error(request,"you cannot perform this action")
        return redirect("signin")

def sign_out_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect("signin")

# PasswordResetView get method=>render a form into a html template :- FORMVIEW

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


