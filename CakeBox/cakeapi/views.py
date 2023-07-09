from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from cakeapp.models import Cakes
from rest_framework import serializers
from rest_framework.decorators import action


class CakeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Cakes
        fields="__all__"


class CakeView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Cakes.objects.all() 
        if "flavour" in request.query_params:
            flav=request.query_params.get("flavour")
            qs=qs.filter(flavour__icontains=flav)

        if "shape" in request.query_params:
            sh=request.query_params.get("shape")
            qs=qs.filter(shape=sh)  
        serializer=CakeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        #serialization
        serializer=CakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakes.objects.get(id=id)
        #deserialization
        serializer=CakeSerializer(qs,many=False)
        return Response(data=serializer.data)  

     #serialization
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Cakes.objects.get(id=id)
        serializer=CakeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)  
        
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Cakes.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")  

    @action(methods=["get"],detail=False) 
    def flavour(self,request,*args,**kwargs): # custom method
        qs=Cakes.objects.all().values_list("flavour",flat=True).distinct()
        return Response(data=qs)