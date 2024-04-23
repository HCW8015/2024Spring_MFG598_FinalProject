from django.urls import path
from . import views

#The urls for the CaloriePage app
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register,name='register'),
    path('login/', views.loginpage,name='login'),
    path('calcom/', views.calcom,name='calcom'),
    path('delete-food/<str:name>', views.DeleteFood, name='delete'),
    path('csvExport', views.csvExport, name='csvExport'),
    path('plotChart/', views.plotChart, name='plotChart')
]
