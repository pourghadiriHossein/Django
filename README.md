# Start Book Store Project

## Create Project without additional folder
```bash
django-admin startproject config .
```

## Create app accounts
### In Windows
```bash
py manage.py startapp accounts
```
### In MacOS
```bash
python manage.py startapp accounts
```
### In Linux
```bash
python3 manage.py startapp accounts
```

## Create templates folder in root
- ### Create _base.html file
```bash 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block page_title %}{% endblock page_title %}</title>
</head>
<body>
{% block content %}
{% endblock content %}
</body>
</html>
```
- ### Create home.html file
```bash 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous" defer></script>
    <style>
        body {
            background-image: linear-gradient(45deg, green, gold);
            background-repeat: no-repeat;
            background-size: cover;
            width: 100%;
            height: 100vh;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>
    <div class="card" style="width: 18rem;">
        <div class="card-body text-center">
            <h3>Home Page</h3>
            <hr>
            {% if user.is_authenticated %}
            <p>Welcome {{ user.username }} | <a class="btn btn-danger" href="{% url 'logout' %}">Logout</a> </p>
            {% else %}
            <a class="btn btn-success" href="{% url 'login' %}">Login</a>
            <a class="btn btn-warning" href="{% url 'signup' %}">Sign Up</a>
            {% endif %}
        </div>
    </div>
</body>
</html>
```
## Create registration folder in root templates
- ### Create login.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
Login
{% endblock page_title %}

{% block content %}
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <button type="submit">
        Login
    </button>
</form>
{% endblock content %}
```

- ### Create signup.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
Sign Up
{% endblock page_title %}

{% block content %}
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <button type="submit">
        Sign Up
    </button>
</form>
{% endblock content %}
```

## Update settings.py file in config
- ### Add two in INSTALLED_APPS
```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]
```
- ### Add Path to TEMPLATES DIR
```bash
str(BASE_DIR.joinpath('templates'))
```
- ### Add Login and Logout Redirect URL and Auth User Model
```bash
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
```

## Update config\urls.py
```bash
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, "home.html" ), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]
```

## accounts app
- ### Update models.py file
```bash
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
```

- ### Create forms.py file
```bash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age', )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
```
- ### Update admin.py file
```bash
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (  
        (None, {'fields': ('age', )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', )}),
    )

    list_display = ['username', 'email', 'age' , 'is_staff']
    list_display_links = ['username', 'email', 'age' , 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
```
- ### Create urls.py file
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up_view, name='signup'), 
]
```

- ### Update views.py file
```bash
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def sign_up_view(request):
    if request.method=='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form })
```

## Make Migrations
- ### In Windows
```bash
py manage.py makemigrations
```
- ### In MacOS
```bash
python manage.py makemigrations
```
- ### In Linux
```bash
python3 manage.py makemigrations
```

## Make Migrate for Project
- ### In Windows
```bash
py manage.py migrate
```
- ### In MacOS
```bash
python manage.py migrate
```
- ### In Linux
```bash
python3 manage.py migrate
```

## Create Super User
- ### In Windows
```bash
py manage.py createsuperuser
```
- ### In MacOS
```bash
python manage.py createsuperuser
```
- ### In Linux
```bash
python3 manage.py createsuperuser
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
