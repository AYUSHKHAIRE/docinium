from django.contrib import admin
from .models import CustomToken, rdpConnection

admin.site.register(CustomToken)
admin.site.register(rdpConnection)
