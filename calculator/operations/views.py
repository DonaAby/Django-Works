from django.shortcuts import render
from django.views.generic import View
from django import forms
from geopy.geocoders import Nominatim
 
def get_address(place):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(place)

def get_location(latitude,longitude):
    geolocator = Nominatim(user_agent="geoapiexerciss")
    getLoc = loc.geocode(latitude,longitude)

class GeolocationForm(forms.Form):
    latitude=forms.IntegerField()
    longitude=forms.IntegerField()

class GeolocationView(View):
    def get(self,request,*args,**kwargs):
        form=GeolocationForm()
        return render(request,"geolocation.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=GeolocationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            lati=form.cleaned_data.get("latitude")
            longi=form.cleaned_data.get("longitude")
            geoLoc = Nominatim(user_agent="GetLoc")
            locname = geoLoc.reverse("26.7674446, 81.109758")
            print(locname.address)
            return render(request,"geolocation.html",{"address":locname.address,"form":form})
        

class OperationForm(forms.Form):
    num1=forms.IntegerField()
    num2=forms.IntegerField()

class ExponentView(View):
    def get(self,request,*args,**kwargs):
        form=OperationForm()
        return render(request,"exponent.html",{"form":form})     
    def post(self,request,*args,**kwargs):
        form=OperationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data) #{"num1":10,"num2":20}
            n1=form.cleaned_data.get("num1")
            n2=form.cleaned_data.get("num2")
            exp=n1**n2
        else:
            print("invalid form")   
       
        return render(request,"exponent.html",{"result":exp,"form":form})

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

class RegisterForm(forms.Form):
    firstname=forms.CharField()
    lastname=forms.CharField()
    email=forms.EmailField()
    username=forms.CharField()
    password=forms.CharField()

class RegisterView(View):
    def get(self,request,*args,**kwargs):
        form=RegisterForm()
        return render(request,"register.html",{"form":form})    
    def post(self,request,*args,**kwargs):
        form=RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print("form is invalid")
        return render(request,"register.html")        

# localhost:8000/add/
class additionView(View):
    def get(self,request,*args,**kwargs):
        form=OperationForm()
        return render(request,"add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        #dict name=request.POST
        form=OperationForm(request.POST)
        if form.is_valid:
            print("valid form")
        else:
            print("invalid form") 
        
        return render(request,"add.html",{"result":res})

# next view:localhost:8000/sub
class substractionView(View):
    def get(self,request,*args,**kwargs):
        form=OperationForm()
        return render(request,"sub.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=OperationForm(request.POST)
        if form.is_valid:
            print("valid form")
        else:
            print("invalid form") 
        return render(request,"sub.html",{"result":res})
    
# localhost:8000/mul
class multiplicationView(View):
    def get(self,request,*args,**kwargs):
        
        return render(request,"mul.html")
    def post(self,request,*args,**kwargs):
        n1=int(request.POST.get("num1"))
        n2=int(request.POST.get("num2"))
        pdt=n1*n2
        return render(request,"mul.html",{"result":pdt})

# localhost:8000/div
class divisionView(View):
    def get(self,request,*args,**kwargs):
        form=OperationForm()
        return render(request,"div.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=OperationForm(request.POST)
        if form.is_valid:
            print("valid form")
        else:
            print("invalid form") 
        return render(request,"div.html",{"result":res})
    

# FACTORIAL OF A NUMBER
class factorialView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"fact.html")
    def post(self,request,*args,**kwargs):
        n=int(request.POST.get("num"))
        fact=1
        for i in range(1,n+1):
            fact=fact*i
        return render(request,"fact.html",{"result":fact})

    
#  PALINDROME NUMBER
class palindromeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"palindrome.html")
    def post(self,request,*args,**kwargs):
        n=int(request.POST.get("num"))
        temp=n
        rev=0
        while temp>0:
          a=temp%10
          rev=(rev*10)+a
          temp=temp//10
          if n==rev:
              answer="Palindrome"
          else:
              answer="Not Palindrome"
        context={"answer":answer}      
        return render(request,"palindrome.html",context)

# ARMSTRONG NUMBER
class armstrongView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"armstrong.html")
    def post(self,request,*args,**kwargs):
        n=int(request.POST.get("num")) 
        l=len(str(n))
        sum=0
        temp=n
        while temp>0:
            a=temp%10
            sum=sum+(a**l)
            temp=temp//10
        if sum==n:
            answer="Armstrong Number"  
        else:
            answer="Not Armstrong Number"    
        context={"answer":answer} 
        return render(request,"armstrong.html",context)  

# PRIME NUMBER
class primeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"prime.html")   
    def post(self,request,*args,**kwargs):
        n=int(request.POST.get("num"))
        f=0
        if n==1 or n==2:
            answer="Not Defined"   
        else:
            for i in range(1,n+1):
                if n%i==0:
                    f=f+1

                if f==2:
                    answer="Prime Number"
                else:
                    answer="Not Prime Number" 
        context={"answer":answer} 
        return render(request,"prime.html",context)    


# EVEN NOS BETWEEN 2 nos
class evenView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"even.html")
    def post(self,request,*args,**kwargs):
        n1=int(request.POST.get("num1"))
        n2=int(request.POST.get("num2"))
        even_no=[i for i in range(n1,n2) if i%2==0]
        # even_no=[]
        # for i in range(n1,n2):
        #     if i%2==0:
        #         even_no.append(i)
        return render(request,"even.html",{"result":even_no})    

# HOME PAGE
class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"home.html")
    

# ASSIGNMENT BODY HEALTH
class bodyView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"body.html")
    def post(self,request,*args,**kwargs):
        t=int(request.POST.get("val1"))
        b=int(request.POST.get("val2"))
        gender=request.POST.get("gender")
        bmi=t/b
        bmi=round(bmi,2)
        print(bmi)
        context={"gender":"","risk":"","body_shape":"","bmi":bmi}
        if gender=="male":
            if bmi<=.95:
                context["gender"]="male"
                context["risk"]="low"
                context["body_shape"]="pear"
            elif bmi>=.96 and bmi<=1:
                context["gender"]="male"
                context["risk"]="moderate"
                context["body_shape"]="avocado"
            elif bmi>1:
                context["gender"]="male"
                context["risk"]="high"
                context["body_shape"]="apple"    
        else:
            if bmi<=.80:
                context["gender"]="female"
                context["risk"]="low"
                context["body_shape"]="pear"

            elif bmi>=.81 and bmi<=.85:
                 context["gender"]="female"
                 context["risk"]="moderate"
                 context["body_shape"]="avocado"

            elif bmi>.85:
                context["gender"]="female"
                context["risk"]="high"
                context["body_shape"]="apple"

        return render(request,"body.html",context)

# ASSIGNMENT TEMPERATURE CONVERSION
class temperatureView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"temp.html")
    def post(self,request,*args,**kwargs):
        t=int(request.POST.get("temp"))
        f=(t*9/5)+32
        return render(request,"temp.html",{"result":f})  
    

class GeoForm(forms.Form):
    place=forms.CharField()

class GeoView(View):
    def get(self,request,*args,**kwargs):
        form=GeoForm()
        return render(request,"geo.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=GeoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            place=form.cleaned_data.get("place")
            address=get_address(place)
            print(address)
        return render(request,"geo.html",{"form":form,"address":address})    


    

