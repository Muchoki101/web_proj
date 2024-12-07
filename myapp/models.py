from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Product(models.Model):
    prod_name = models.CharField(max_length=100)
    prod_price = models.IntegerField()
    prod_category = models.CharField(max_length=100)
    prod_qty = models.IntegerField()
    prod_img = models.ImageField(upload_to='products/')
    prod_desc = models.CharField(max_length=100)



class Users(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

def __str__(self):
        return self.title