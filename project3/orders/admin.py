from django.contrib import admin

from .models import ProductCategory, ProductExtra, Product, PriceList, Customer, Order, OrderItem

admin.site.register(ProductCategory)
admin.site.register(ProductExtra)
admin.site.register(Product)
admin.site.register(PriceList)
admin.site.register(Customer)
admin.site.register(OrderItem)

