from django.contrib import admin

from .models import ProductCategory, ProductExtra, Product, PriceList, Order, OrderItem

admin.site.register(ProductCategory)
admin.site.register(ProductExtra)
admin.site.register(Product)
admin.site.register(PriceList)
admin.site.register(OrderItem)
admin.site.register(Order)


