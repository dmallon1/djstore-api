from django.contrib import admin
from store.models import Product, Order, ProductInstance

class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'sku')

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductInstance, ProductInstanceAdmin)
