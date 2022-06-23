from django.contrib import admin

# Register your models here.
from .models import Products
admin.site.register(Products)

from .models import Students
admin.site.register(Students)