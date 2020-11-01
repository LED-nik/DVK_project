from django.contrib import admin
from .models import Item, Order, Address, CreditCard

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(CreditCard)
