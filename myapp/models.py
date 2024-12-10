from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    prod_name = models.CharField(max_length=100)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)
    prod_category = models.CharField(max_length=100)
    prod_qty = models.IntegerField()
    prod_img = models.ImageField(upload_to='products/')
    prod_desc = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prod_name

class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.product.prod_name} - {self.quantity}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"


class Users(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    pass

def __str__(self):
        return self.title