from django.db import models



class Vehicle(models.Model):
    name=models.CharField(max_length=250)
    number=models.CharField(max_length=250)
    fueltype=models.CharField(max_length=250)
    wheel=models.CharField(max_length=100)
    color=models.CharField(max_length=100)

    def _str_(self):
        return self.name
