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

 