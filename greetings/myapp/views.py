from django.shortcuts import render
from django.views.generic import View

# localhost:8000/morning/
#get

class GoodMorningView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"morning.html")

class GoodAfternoonView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"afternoon.html") 

class GoodEveningView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"evening.html")   

class GoodNightView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"night.html")    