from django.contrib import admin
from .models import MenuItem, Ingredient, Purchase

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Ingredient)
admin.site.register(Purchase)