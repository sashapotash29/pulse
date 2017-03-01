from django.contrib import admin
from .models import Hit, Company

# Register your models here.

admin.site.register(Company)
admin.site.register(Hit)