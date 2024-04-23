from django.contrib import admin
from .models import caloriesConsumption

# Register your models here.

#Register the caloriesConsumption model so you can edit it in the admin page
admin.site.register(caloriesConsumption)