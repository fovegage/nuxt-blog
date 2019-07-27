from django.contrib import admin
from .models import UserMessage, UserFav

admin.site.register(UserMessage)
admin.site.register(UserFav)
