from django.db import models

class Vehicles(models.Model):
    name=models.CharField(max_length=250)
    model=models.CharField(max_length=200)
    category=models.CharField(max_length=240)
    owner_type=models.CharField(max_length=250)
    fuel_type=models.CharField(max_length=200)
    kms=models.CharField(max_length=220)
    price=models.PositiveBigIntegerField()
    description=models.CharField(max_length=240)
    vehicle_number=models.CharField(max_length=200,unique=True)
    def __str__(self):
        return self.name

class Mobiles(models.Model):
    name=models.CharField(max_length=200)
    brand=models.CharField(max_length=220) 
    price=models.PositiveBigIntegerField()
    display=models.CharField(max_length=250, default="lcd")
    def __str__(self):
        return self.name   

class Movies(models.Model):
    name=models.CharField(max_length=200)
    genres=models.CharField(max_length=250)
    year=models.CharField(max_length=100)
    language=models.CharField(max_length=220)
    rating=models.CharField(max_length=290)
    def __str__(self):
        return self.name
