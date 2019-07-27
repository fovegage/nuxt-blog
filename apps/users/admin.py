from django.contrib import admin
from .models import UserInfo, VerifyCode, UserAddress

admin.site.register(UserAddress)
admin.site.register(VerifyCode)
admin.site.register(UserInfo)