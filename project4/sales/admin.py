from django.contrib import admin

from .models import Customer, Product, Opportunity, OpportunityProduct

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Opportunity)
admin.site.register(OpportunityProduct)
