# Update Accounts App And Complate Login, Sign Up and Logout Progres

## accounts app
- ### Update forms.py File
```bash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('phone', 'status')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class Login(forms.Form):
    phone = forms.CharField(required=True, min_length=11, max_length=14,
    error_messages={
        'required' : 'شماره تماس خود را وارد کنید',
        'min_length' : 'شماره تماس شما نمی تواند کمتر از 11 کاراکتر باشد',
        'max_length' : 'شماره تماس شما نمی تواند بیشتر از 14 کاراکتر باشد',
    })
    password = forms.CharField(required=True, min_length=4, max_length=100,
    error_messages={
        'required' : 'رمز عبور خود را وارد کنید',
        'min_length' : 'رمز عبور شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'رمز عبور شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })

class SignUp(forms.Form):
    name = forms.CharField(required=True, min_length=4, max_length=100,
    error_messages={
        'required' : 'نام کاربری خود را وارد کنید',
        'min_length' : 'نام کاربری شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'نام کاربری شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })
    phone = forms.CharField(required=True, min_length=11, max_length=14,
    error_messages={
        'required' : 'شماره تماس خود را وارد کنید',
        'min_length' : 'شماره تماس شما نمی تواند کمتر از 11 کاراکتر باشد',
        'max_length' : 'شماره تماس شما نمی تواند بیشتر از 14 کاراکتر باشد',
    })
    email = forms.CharField(required=True, min_length=10, max_length=100,
    error_messages={
        'required' : 'پست الکترونیک خود را وارد کنید',
        'min_length' : 'پست الکترونیک شما نمی تواند کمتر از 10 کاراکتر باشد',
        'max_length' : 'پست الکترونیک شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })
    password = forms.CharField(required=True, min_length=4, max_length=100,
    error_messages={
        'required' : 'رمز عبور خود را وارد کنید',
        'min_length' : 'رمز عبور شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'رمز عبور شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })
```
- ### Update views.py File
```bash
from django.shortcuts import render, redirect
from django.urls import resolve
from shop import models
from django.contrib.auth import authenticate, login as loginRequest, logout as logoutRequest
from .forms import Login, SignUp
from django.contrib import messages
from .models import CustomUser
from lib import error_progres

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            password = request.POST['password']
            user = CustomUser.objects.filter(phone=phone).first()
            if user:
                login_user = authenticate(username=user.username, password=password)
                if login_user is not None:
                    loginRequest(request, login_user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'رمز عبور صحیح نیست')   
            else:
                messages.error(request, 'کاربری با این شماره تماس وجود ندارد')    
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)

    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
    }
    return render(request, 'registration/login.html', context)

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            username = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            password = request.POST['password']
            username_state = False
            phone_state = False
            email_state = False
            if CustomUser.objects.filter(username=username).first():
                messages.error(request, 'نام کاربری مورد نظر قبلا ثبت شده است')
                username_state = True
            if CustomUser.objects.filter(phone=phone).first():
                messages.error(request, 'شماره تماس مورد نظر قبلا ثبت شده است')
                phone_state = True
            if CustomUser.objects.filter(email=email).first():
                messages.error(request, 'پست الکترونیک مورد نظر قبلا ثبت شده است')
                email_state = True
            if (username_state == False and phone_state == False and email_state == False):
                new_user = CustomUser.objects.create(
                    username = username,
                    phone = phone,
                    email = email,
                )
                new_user.set_password(password)
                new_user.save()
                loginRequest(request, new_user)
                return redirect('dashboard')    
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'registration/signup.html', context)

def logout(request):
    if request.user.is_authenticated:
        logoutRequest(request)
        return redirect('home')
    else:
        return redirect('login')
```
## Create lib Folder
- ### Create __init__.py File
```bash
from lib.error_handling import *
```
- ### Create error_handling.py File
```bash
def error_progres(errors):
    error_messages = []    
    for error in errors:
        error_messages.append(errors[error][0])
    return error_messages
```
## Root templates Folder
- ### In registration Folder, login.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Login.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox login">
    <h1>ورود</h1>
    <hr>
    <div class="loginBox">
        {% if messages %}
        <ul class="message-box">
            {% for message in messages %}
            <li class="alert alert-{{message.tags}}">{{message}}</li>
            {% endfor %}
        </ul>
        {% endif %}
        <form action="{% url 'login' %}" method="POST" autocomplete="on">
            {% csrf_token %}
            <input type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
            <input type="password" name="password" placeholder="رمز عبور خود را وارد کنید">
            <input type="submit" value="ارسال کن">
        </form>
    </div>
    <div class="guideBox">
        <p>فرم آزمایشی پروژه پل استار جهت آموزش بهتر و کاردبری تر با ضاهر مناسب جهت ارتباط گیری بیشتر با مبحث تحصیلی می باشد</p>
        <p>شماره تماس: 34911-013</p>
        <p>آدرس: گیلان - رشت - گلسار - چهار راه اصفهان</p>
        <p>پست الکترونیک: info@poulstar.com</p>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```
- ### In registration Folder, signup.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Register.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox register">
    <h1>ثبت نام</h1>
    <hr>
    <div class="registerBox">
        {% if messages %}
        <ul class="message-box">
            {% for message in messages %}
            <li class="alert alert-{{message.tags}}">{{message}}</li>
            {% endfor %}
        </ul>
        {% endif %}
        <form action="{% url 'sign_up' %}" method="POST" autocomplete="on">
            {% csrf_token %}
            <input type="text" name="name" placeholder="نام و نام خانوادگی خود را وارد کنید">
            <input type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
            <input type="text" name="email" placeholder="پست الکترونیک خود را وارد کنید">
            <input type="password" name="password" placeholder="رمز عبور خود را وارد کنید">
            <input type="submit" value="ارسال کن">
        </form>
    </div>
    <div class="guideBox">
        <p>فرم آزمایشی پروژه پل استار جهت آموزش بهتر و کاردبری تر با ضاهر مناسب جهت ارتباط گیری بیشتر با مبحث تحصیلی می باشد</p>
        <p>شماره تماس: 34911-013</p>
        <p>آدرس: گیلان - رشت - گلسار - چهار راه اصفهان</p>
        <p>پست الکترونیک: info@poulstar.com</p>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```

## Run Your App
- ### In Windows
```bash
py manage.py runserver
```
- ### In MacOS
```bash
python manage.py runserver
```
- ### In Linux
```bash
python3 manage.py runserver
```
