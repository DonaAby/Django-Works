from django.db import models


from django.contrib.auth.models import User

class Movie(models.Model):
    
    movie_name=models.CharField(max_length=100)
    year=models.CharField(max_length=100)
    genres=models.CharField(max_length=200)
    runtime=models.CharField(max_length=150)
    language=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",null=True,blank=True)

    def __str__(self):
        return self.name



