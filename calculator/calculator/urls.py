"""calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from operations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/',views.additionView.as_view(),name="add"),
    path('sub/',views.substractionView.as_view(),name="sub"),
    path('mul/',views.multiplicationView.as_view(),name="mul"),
    path('div/',views.divisionView.as_view(),name="div"),
    path('fact/',views.factorialView.as_view(),name="fact"),
    path('palindrome/',views.palindromeView.as_view(),name="palindrome"),
    path('armstrong/',views.armstrongView.as_view(),name="armstrong"),
    path('prime/',views.primeView.as_view(),name="prime"),
    path('even/',views.evenView.as_view(),name="even"),
    path('body/',views.bodyView.as_view(),name="body"),
    path('temp/',views.temperatureView.as_view(),name="temp"),
    path('exponent/',views.ExponentView.as_view(),name="exponent"),
    path('login/',views.LoginView.as_view(),name="login"),
    path("register/",views.RegisterView.as_view(),name="register"),
    path("geo/",views.GeoView.as_view()),
    path("geolocation/",views.GeolocationView.as_view()),
    path("",views.HomeView.as_view(),name="home")

]
