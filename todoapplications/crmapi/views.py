from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from crm.models import Employee
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import authentication,permissions

# serializer=> convert queryset to python natives
class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee
        fields="__all__"

class EmployeesView(ViewSet):
    # list,create,retrieve,update,destroy
    
    # localhost:8000/api/employee/
    # method GET
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department__icontains=dept)

        if "salary" in request.query_params:
            sal=request.query_params.get("salary")
            qs=qs.filter(salary=sal)  

        if "salary_gt" in request.query_params:
            sal=request.query_params.get("salary_gt")
            qs=qs.filter(salary__gte=sal) 

        #deserialization
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data) 
    
    # localhost:8000/api/employees
    # method POST
    def create(self,request,*args,**kwargs):
        #serialization
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    # localhost:8000/api/employees/{id}/
    # method GET
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        #deserialization
        serializer=EmployeeSerializer(qs,many=False)
        return Response(data=serializer.data)

    # localhost:8000/api/employees/{id}/
    # method PUT
    #serialization
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    
    # localhost:8000/api/employees/delete
    # method DESTROY
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")

    #localhost:8000/api/employees/departments/    
    @action(methods=["get"],detail=False) 
    def departments(self,request,*args,**kwargs): # custom method
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs)
    
#MODELVIEWSET
class EmployeeViewsetView(ModelViewSet):
    serializer_class=EmployeeSerializer
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]
