from django.db import models

class Cakes(models.Model):
    name=models.CharField(max_length=210)
    flavour=models.CharField(max_length=270)
    price=models.IntegerField()
    shape=models.CharField(max_length=250)
    weight=models.CharField(max_length=200)
    layer=models.CharField(max_length=240)
    number=models.IntegerField()
    description=models.CharField(max_length=280)
    picture=models.ImageField(upload_to="images",null=True,blank=True)

    def __str__(self):
        return self.name
