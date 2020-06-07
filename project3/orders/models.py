from django.db import models

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class ProductExtra(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    productcategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="productcategoryproductextra")
    
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=50)
    productcategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="productcategoryproduct")
    hasExtra = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.productcategory} - {self.name}"

class PriceList(models.Model):
    size = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productpricelist")

    def __str__(self):
        return f"{self.product}"

class Order(models.Model):
    customer = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    total = models.DecimalField(decimal_places=2,max_digits=10)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer} - {self.description} - {self.total} - {self.status}"

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

