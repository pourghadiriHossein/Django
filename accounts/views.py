from django.shortcuts import render
from django.urls import resolve
from shop import models

def login(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'registration/login.html', context)

def sign_up(request):
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
    return True