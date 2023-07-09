from django.db import models
from django.contrib.auth.models import User

class Occassion(models.Model):
    name=models.CharField(max_length=250)

class Cake(models.Model):
    name=models.CharField(max_length=250,unique=True)
    occassion=models.ForeignKey(Occassion,on_delete=models.CASCADE)
    options=(("round","round"),
             ("square","square"),
             ("heart","heart"))
    shape=models.CharField(max_length=200,choices=options,default="square")
    layers=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    weight=models.PositiveIntegerField()
    flavour=models.CharField(max_length=200)

class CakeImage(models.Model):
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)  
    img=models.ImageField(null=True,blank=True)

class Cart(models.Model):
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=300)
    created_date=models.DateTimeField()

class Order(models.Model):
    cake=models.ForeignKey(Cart,on_delete=models.CASCADE)
    created_date=models.DateTimeField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=300)
    status=models.CharField(max_length=300)
    expected_delivery_date=models.DateTimeField()

class Reviews(models.Model):
    cake=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.PositiveIntegerField()

    

