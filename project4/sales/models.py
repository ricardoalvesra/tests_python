from django.db import models

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    address3 = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.name}"

class Opportunity(models.Model):
    topic = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    estimateclosedate = models.DateField()

    def __str__(self):
        return f"{self.topic}"

class OpportunityProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2,max_digits=10)
    totalamount = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.product}"

