from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import caloriesConsumption
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import csv


#5wQQ3p0lqaaPdTlYjWRurQ==NlrOuWQBRVxTAoUD
# Create your views here.

#exporting data to csv
def csvExport(request): 
    foodData = caloriesConsumption.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=foodData.csv'
    writer = csv.writer(response)
    writer.writerow([ 'User','Food Name', 'Food Calorie'])
    foodDataFields = foodData.values_list('user', 'foodName', 'foodCalorie')
    for food in foodDataFields:
        writer.writerow(food)
    return response

#The food search page, where the user can search for food and get the calorie content of the food, using the API
def home(request):
    if request.method == "POST":
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get (api_url + query, headers = {'X-Api-Key': '5wQQ3p0lqaaPdTlYjWRurQ==NlrOuWQBRVxTAoUD'})
        try:
            #load the api request content into json
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "Somthing wrong with this api"
            #see the api content
            print(api)
        return render(request, 'home.html',{'api':api})
    else: 
        return render(request, 'home.html',{'query':'Please enter a valid query'})
    
#The calorie record page, where the user can see the food they have consumed and record it, and also export the data to a csv file
def calcom(request):
    foodCalorie = None
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get (api_url + query, headers = {'X-Api-Key': '5wQQ3p0lqaaPdTlYjWRurQ==NlrOuWQBRVxTAoUD'})
        try:
            api = json.loads(api_request.content)
            #print(api_request.content)
            #see the food and calorie content
            print(api[0]['calories'])
            print(api[0]['name'])
        except Exception as e:
            api = "Oops! Somthing wrong with this api"
            print(api)
        #save the food and calorie content to the database using numpy
        food = np.array(api[0]['name'])
        foodCalorie = np.array(api[0]['calories'])
        newFood = caloriesConsumption(user=request.user, foodName= food, foodCalorie=foodCalorie)
        newFood.save()

    #get all the food items consumed by the user
    allFoods = caloriesConsumption.objects.filter(user=request.user)
    context = {
        'foods': allFoods,
        'foodCalorie': foodCalorie              
    }
    return render(request, 'calcom.html', context)

#The user registration page
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 6:
            messages.error(request, 'Password is too short. Pls try again and input more than 6 characters.')
            return redirect('register')
        
        getAllUsersByUsername = User.objects.filter(username=username)
        if getAllUsersByUsername:
            messages.error(request, 'Error! user already exists, try again pls.')
            return redirect('register')
        
        #create a new user
        newUser = User.objects.create_user(username=username, email=email, password=password)
        newUser.save()
        messages.success(request,'User successfully created, login now.')
        return redirect('login')
    return render(request, 'register.html', {})

#The user logout page
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        #authenticate the user
        validateUser = authenticate(username=username, password=password)
        if validateUser is not None:
            login(request, validateUser)
            return redirect('home')
        else:
            messages.error(request, 'Error! check your password or user does not exist.')
            return redirect('login')
    return render(request, 'login.html', {})    

#If user wants to delete a food item from the list
def DeleteFood(request,name):
    getFood = caloriesConsumption.objects.get(user=request.user,foodName=name)
    getFood.delete()
    return redirect('calcom')

    
#If user wants to plot a chart of the food items consumed
def plotChart(request):
    allFoods = caloriesConsumption.objects.filter(user=request.user)
    foodNames = np.array([food.foodName for food in allFoods])
    foodCalories = np.array([food.foodCalorie for food in allFoods])
    plt.pie(foodCalories, labels=foodNames, autopct='%1.1f%%')
    plt.title('Calorie Consumption Chart')
    plt.legend(loc='upper right', labels=foodNames)
    plt.tight_layout()
    plt.show()
    return redirect('calcom')
    