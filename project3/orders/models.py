from django.db import models

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
    
    def __str__(self):
        return f"{self.name} - {self.productcategory}"

class PriceList(models.Model):
    size = models.CharField(max_length=1)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productpricelist")

    def __str__(self):
        return f"{self.product}"

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    emailaddress = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firstname} - {self.lastname}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customerorder")
    total = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.customer} - {self.total}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productorderitem")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderorderitem")
    price = models.DecimalField(decimal_places=2,max_digits=10)
    extras = models.ManyToManyField(ProductExtra, blank=True, related_name="productextras")

    def __str__(self):
        return f"{self.product} - {self.price}"

