from django.contrib import admin

# Register your models here.
from stock.models import Product, Vendor, Customer

admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Customer)

