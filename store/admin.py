from django.contrib import admin
from store.models import Product, Order, ProductInstance, ShirtSize, ProductInstance

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductInstance)
admin.site.register(ShirtSize)
