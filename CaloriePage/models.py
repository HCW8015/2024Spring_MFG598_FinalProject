from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#The model for the caloriesConsumption
class caloriesConsumption(models.Model):
    #The user who consumed the food
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #The name of the food
    foodName = models.CharField(max_length=200)
    #The status of the food(unuse)
    status = models.BooleanField(default=False)
    #The calorie content of the food
    foodCalorie = models.TextField(null = True, blank = True)
    def __str__(self):
        return self.foodName
    class Meta:
        ordering = ['status']