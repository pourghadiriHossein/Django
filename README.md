# Login and Register Process

## Create registration Folder in Base templates Folder 
- ### Create login.html File
```bash
{% extends '_base.html' %}

{% block title %}
    Login
{% endblock title %}

{% block content %}
    <div class="container p-5">
        <div class="card shadow p-5">
            <form action="", method="post">
                {% csrf_token %}
                <table>
                    {{ form.as_table }}
                </table>
                <input class="btn btn-success" type='submit', value='Login'>
            </form>
        </div>
    </div>
{% endblock content %}
```
- ### Create signup.html
```bash
{% extends '_base.html' %}

{% block title %}
    Sign Up
{% endblock title %}

{% block content %}
    <div class="container p-5">
        <div class="card shadow p-5">
            <form action="", method="post">
                {% csrf_token %}
                <table>
                    {{ form.as_table }}
                </table>
                <input class="btn btn-success" type='submit', value='Sign Up'>
            </form>
        </div>
    </div>
{% endblock content %}
```

## Update _base.html in Base templates Folder 
```bash
<div class="mx-1">
    {% if user.is_authenticated %}
        <span> Welcome {{ user.username }} </span> | <a href="{% url 'logout' %}" style="color: #222"> Logout </a>
    {% else %}
        <a href="{% url 'login' %}" style="color: #222">Login</a> | <a href="{% url 'signup' %}" style="color: #222"> Sign Up </a>
    {% endif %}
</div>
```

## Update settings.py 
- ### add login and register url redirect
```bash
LOGIN_REDIRECT_URL = 'posts_list'
LOGOUT_REDIRECT_URL = 'login'
```

## Add Two Path in urls.py File in config
```bash
path('accounts/', include('django.contrib.auth.urls')),
path('accounts/', include('accounts.urls')),
```

## Create urls.py file in accounts app
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up_view, name='signup'),
]
```

## Create sing up function in accounts app urls.py file
```bash
from django.shortcuts import render, redirect
from django.contrib.auth import forms

def sign_up_view(request):
    if request.user.is_authenticated:
        return redirect('posts_list') 
    if request.method=='POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = forms.UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form })
```

## Update Some Function in blog app views.py app
- ### Add authenticated Condition for post_create_view function and post_update_view function and post_delete_view function
```bash
 if not request.user.is_authenticated:
    return redirect('posts_list')
```

## Add authenticated Condition to Update and Delete button in post_detail.html file in blog app templates
```bash
{% if user.is_authenticated %}
<div>
    <a href = "{% url 'update' post.id %}" class="btn btn-sm btn-warning">Update</a>
    <a href = "{% url 'delete' post.id %}" class="btn btn-sm btn-danger">Delete</a>
</div>
{% endif %}
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
