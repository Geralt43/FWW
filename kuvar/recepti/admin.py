from django.contrib import admin
from .models import Recipe ,Rating, Ingredient

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Rating)
