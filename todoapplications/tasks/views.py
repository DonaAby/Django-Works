from django.shortcuts import render,redirect
from django.views.generic import View
from django import forms
from tasks.models import Todo

class TodoForm(forms.Form):
    task_name=forms.CharField()
    user=forms.CharField()

class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Todo.objects.create(**form.cleaned_data)   # ** to unpack dictionary
            return redirect("todo-list")
        return render(request,"todo-add.html",{"form":form})  
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(status=False).order_by("-date") # sorting the todos in descending order
        return render(request,"todo-list.html",{"todos":qs}) 

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,"todo-detail.html",{"todo":qs})  

class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        return redirect("todo-list")
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.filter(id=id).update(status=True)
        return redirect("todo-list")
    
class TaskFinishView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(status=True)
        return render(request,"todo-finish.html",{"todos":qs})

        
