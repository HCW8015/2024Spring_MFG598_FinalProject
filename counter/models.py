from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class caloriesConsumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    foodName = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    foodCalorie = models.TextField(null = True, blank = True)
    def __str__(self):
        return self.foodName
    class Meta:
        ordering = ['status']