from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from todoapi.serializers import UserSerializer,TodoSerializer
from django.contrib.auth.models import User
from tasks.models import Todo
from rest_framework import authentication,permissions

class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    model=User
    # by default create,list,retrieve, update,destroy

    # works when POST given through THUNDER CLIENT
    # def create(self,request,*args,**kwargs):
    #     serializer=UserSerializer(data=request.data)  #serialization
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer.validated_data)
    #         serializer=UserSerializer(usr) #deserialization
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

class TodosView(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todo.objects.all()
    #authentication_classes=[authentication.BasicAuthentication] 
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    # to list only the logged in user we override the list method
    # def list(self,request,*args,**kwargs):
    #     qs=Todo.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)    

    # another method by changing query
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
       


