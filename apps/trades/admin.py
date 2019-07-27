from django.contrib import admin
from .models import OrderInfo, PayInfo, ShoppingCart

admin.site.register(OrderInfo)
admin.site.register(PayInfo)
admin.site.register(ShoppingCart)
