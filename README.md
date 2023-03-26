# Learn Crispy and Password Recovery Proccessiong in Book Store Project

## Create app pages
### In Windows
```bash
py manage.py startapp pages
```
### In MacOS
```bash
python manage.py startapp pages
```
### In Linux
```bash
python3 manage.py startapp pages
```

## templates folder in root
- ### Update _base.html file
```bash 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block page_title %}{% endblock page_title %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous" defer></script>
</head>
<body>
    <div class='container mt-5'>
        {% block content %}
        {% endblock content %}
    </div>
</body>
</html>
```

## registration folder in root templates
- ### Update login.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Login
{% endblock page_title %}

{% block content %}
<h1>
    Login
</h1>
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success mt-3'>
        Login
    </button>
</form>
<p>
    <a href="{% url 'password_reset' %}">Forgot Password</a>
    |
    <a href="{% url 'signup' %}">Sign Up</a>
</p>
{% endblock content %}
```

- ### Update signup.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Sign Up
{% endblock page_title %}

{% block content %}
<h1>
    Sign Up
</h1>
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success'>
        Sign Up
    </button>
</form>
<a class='btn btn-outline-warning mt-3' href="{% url 'login' %}">Login</a>
{% endblock content %}
```
- ### Create password_reset_form.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Password Reset
{% endblock page_title %}

{% block content %}
<h1>
    Password Reset
</h1>
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success mt-3'>
        Send Email
    </button>
</form>
{% endblock content %}
```
- ### Create password_reset_done.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
Password Reset Done
{% endblock page_title %}

{% block content %}
<h1>
    Password Reset
</h1>
<h2>
    Email Sent
</h2>
<p>
    Check your email!
</p>
{% endblock content %}
```
- ### Create password_reset_email.html file
```bash
Hello, {{ user.username }}

Someone just asked for password reset of this email: {{ email }}

If it was you that asked for this link, please click on the link below:

{{ protocol }}://{{ domain }}{%url 'password_reset_confirm' uidb64=uid token=token %}

If you forgot your username: {{ user.username }}
Thanks for using our website.

Poulstar
```
- ### Create password_reset_confirm.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Set New Password
{% endblock page_title %}

{% block content %}
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success mt-3'>
        Update Password
    </button>
</form>
{% endblock content %}
```
- ### Create password_change_done.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
Password Change Successful
{% endblock page_title %}

{% block content %}
<h1>
    Password Changed Successfully!
</h1>
{% endblock content %}
```
- ### Create password_reset_complete.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
Successful Reset of Password
{% endblock page_title %}

{% block content %}
<h1>
    Reset Completed Successfully
</h1>
<p>
    Login And Enjoy
</p>
<p>
    You can login <a href="{% url 'login' %}">here</a>
</p>
{% endblock content %}
```
- ### Create password_change_form.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Password Change
{% endblock page_title %}

{% block content %}
<form action="" method="POST" class="mt-3">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success mt-3'>
        Change
    </button>
</form>
{% endblock content %}
```

## Crispy
- ### Install Django Crispy Forms
```bash
pip install django-crispy-forms
```
- ### Install Crispy Bootstrap5
```bash
pip install crispy-bootstrap5
```
- ### Add Two App in INSTALLED_APPS in config\settings.py
```bash
INSTALLED_APPS = [
    ...,
    'crispy_forms',
    'crispy_bootstrap5',
]
```
- ### Add Two Variable in config\settings.py
```bash
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

- ### When You Need Load Crispy in Django Template
```bash
{% load crispy_forms_tags %}
```

- ### Sample Crispy Code
```bash
{{ form|crispy }}
```

## Update settings.py file in config
- ### Add Crispy in INSTALLED_APPS
```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'pages',
    'crispy_forms',
    'crispy_bootstrap5',
]
```

- ### Add Email Config
```bash
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
- ### Add Crispy Variable
```bash
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

## Update config\urls.py
```bash
from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', lambda request: render(request, "home.html" ), name='home'),
    path('', include('pages.urls')),
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
