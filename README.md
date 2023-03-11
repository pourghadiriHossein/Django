# how to Load Image, CSS, Java Script File in Django Template

## <a href="https://www.w3schools.com/django/django_create_virtual_environment.php">Create Virtual Environment</a>
### In Windows
```bash
py -m venv myVenvName
```
### In MacOS
```bash
python -m venv myVenvName
```
### In Linux
```bash
python3 -m venv myVenvName
```

## cd Current venv
### In Windows cmd
```bash
myVenvName\Scripts\activate.bat
```
### In MacOS
```bash
source myVenvName/bin/activate
```
### In Linux
```bash
source myVenvName/bin/activate
```

## <a href="https://www.w3schools.com/django/django_install_django.php">Install Django</a>
### In Windows
```bash
py -m pip install Django
```
### In MacOS
```bash
python -m pip install Django
```
### In Linux
```bash
python3 -m pip install Django
```

## <a href="https://www.w3schools.com/django/django_create_project.php">Django Create Project</a>
### Create Project without additional folder
```bash
django-admin startproject config .
```

## Create app homePage
### In Windows
```bash
py manage.py startapp homePage
```
### In MacOS
```bash
python manage.py startapp homePage
```
### In Linux
```bash
python3 manage.py startapp homePage
```

## set new app in config\settings.py - insert 'homePage'

## Link homePage in config\urls.py
```bash
from django.urls import include
```
```bash
add path('homePage/', include('homePage.urls'))
```

## Create templates Folder in homePage App
- ### Create index.html File

## Create static Folder in homePage App
- ### Create css Folder, then Create style.css
- ### Create js Folder, then Create main.js
- ### Create image Folder, then Add Four Image For Slide Show and One Image For Logo

## Create urls.py file in homePage
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]
```

## Write hello function for homePage views.py
```bash
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
```


## load Static File Command In Django Template
```bash
{% load static %}
```


## How to Load Static File in href Or src In Django Template
```bash
{% static 'folder-name/file-name.extension' %}
```

## Run Your App
### In Windows
```bash
py manage.py runserver
```
### In MacOS
```bash
python manage.py runserver
```
### In Linux
```bash
python3 manage.py runserver
```

## Simple HTML Template
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{WEB SITE TITLE}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="{YOUR CSS LINK}">
    <script src="{YOUR JS LINK}" defer></script>
</head>
<body>
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark" id="nav">
        <div class="container-fluid">
            <a class="navbar-brand" href="javascript:void(0)">
                <img src="{YOUR IMAGE PATH}" alt="logo" width="40px">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsibleNavbar">
            <ul class="navbar-nav">
                <li class="nav-item">
                <a class="nav-link text-light" href="javascript:void(0)" onclick="red()">Red</a>
                </li>
                <li class="nav-item">
                <a class="nav-link text-light" href="javascript:void(0)" onclick="blue()">Blue</a>
                </li>
                <li class="nav-item">
                <a class="nav-link text-light" href="javascript:void(0)" onclick="yellow()">Yellow</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-light" href="javascript:void(0)" onclick="cyan()">Cyan</a>
                </li>  
                <li class="nav-item">
                    <a class="nav-link text-light" href="javascript:void(0)" onclick="gray()">Gray</a>
                </li>    
            </ul>
            </div>
        </div>
    </nav>
    <div id="demo" class="carousel slide" data-bs-ride="carousel">

        <!-- Indicators/dots -->
        <div class="carousel-indicators">
          <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
          <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
          <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
          <button type="button" data-bs-target="#demo" data-bs-slide-to="3"></button>
        </div>
        
        <!-- The slideshow/carousel -->
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img src="{YOUR IMAGE PATH}" alt="image1" class="d-block" style="width:100%; height: 93vh;">
          </div>
          <div class="carousel-item">
            <img src="{YOUR IMAGE PATH}" alt="image2" class="d-block" style="width:100%; height: 93vh;">
          </div>
          <div class="carousel-item">
            <img src="{YOUR IMAGE PATH}" alt="image3" class="d-block" style="width:100%; height: 93vh;">
          </div>
          <div class="carousel-item">
            <img src="{YOUR IMAGE PATH}" alt="image4" class="d-block" style="width:100%; height: 93vh;">
          </div>
        </div>
        
        <!-- Left and right controls/icons -->
        <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
          <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
          <span class="carousel-control-next-icon"></span>
        </button>
    </div>
</body>
</html>
```

