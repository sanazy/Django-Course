from django.contrib import admin

from accounts.models import Customer
from market.models import Product, OrderRow, Order

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderRow)
admin.site.register(Order)
