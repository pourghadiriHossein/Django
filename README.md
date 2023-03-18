# How To Create Multi Route In Django

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

## Create app car
### In Windows
```bash
py manage.py startapp car
```
### In MacOS
```bash
python manage.py startapp car
```
### In Linux
```bash
python3 manage.py startapp car
```

## Create app football
### In Windows
```bash
py manage.py startapp football
```
### In MacOS
```bash
python manage.py startapp football
```
### In Linux
```bash
python3 manage.py startapp football
```

## Create app musicBand
### In Windows
```bash
py manage.py startapp musicBand
```
### In MacOS
```bash
python manage.py startapp musicBand
```
### In Linux
```bash
python3 manage.py startapp musicBand
```

## set new app in config\settings.py - insert 'car' , 'football' , 'musicBand'

## Link All App in config\urls.py
```bash
from django.urls import include
```
```bash
path('car/', include('car.urls')),
path('football/', include('football.urls')),
path('musicBand/', include('musicBand.urls')),
```


## Create urls.py file in car
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bmw/', views.bmw, name='bmw'),
    path('benz/', views.benz, name='benz'),
    path('dodge/', views.dodge, name='dodge'),
]
```

## Create urls.py file in football
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ronaldo/', views.ronaldo, name='ronaldo'),
    path('messi/', views.messi, name='messi'),
    path('karim/', views.karim, name='karim'),
]
```

## Create urls.py file in musicBand
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('BTS/', views.BTS, name='BTS'),
    path('Queen/', views.Queen, name='Queen'),
    path('Pink-Floyd/', views.Pink_Floyd, name='Pink_Floyd'),
]
```

## Write Necessary function for car, football, musicBand in views.py
```bash
from django.shortcuts import render
from django.http import HttpResponse
def home(request):
  return HttpResponse(''' {YOUR HTML FILE} ''')
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

## Simple HTML Template For Index
```bash
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{YOUR WEB PAGE NAME}</title>
        <style>
            * {
              outline: 0;
              margin: 0;
              border: 0;
              padding: 0;
              box-sizing: border-box;
            }
            body {
              background-image: url({INSERT YOUR IMAGE PATH FOR BACKGROUND});
              background-size: cover;
              background-repeat: no-repeat;
            }
            .list-background {
              width: 40%;
              margin: 2% auto;
              min-height: 400px;
              background-color: rgba(240, 240, 240, 0.5);
              padding: 2%;
              text-align: center;
            }
            .guide {
              font-size: xx-large;
              font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
              font-weight: bold;
              margin: 3% 0;
            }
            .list {
              list-style: none;
            }
            .item {
              font-size: 26px;
              font-weight: bold;
              font-style: italic;
              font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
              letter-spacing: 2px;
              margin: 5% auto;
              background-image: linear-gradient(to left, rgb(189, 51, 189), rgb(103, 207, 207));
              width: 40%;
              padding: 3%;
              border-radius: 4px;
              color: white;
            }
        </style>
    </head>
    <body>
        <div class="list-background">
            <p class="guide">Use This List Music Band In Route</p>
            <ul class="list">
              <li class="item">{WRITE YOUR SUB DOMAIN NAME}</li>
              <li class="item">{WRITE YOUR SUB DOMAIN NAME}</li>
              <li class="item">{WRITE YOUR SUB DOMAIN NAME}</li>
            </ul>
        </div>
    </body>
</html>
```

## Simple HTML Template For Sub Domain
```bash
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{YOUR WEB PAGE NAME}</title>
        <style>
            * {
              outline: 0;
              margin: 0;
              border: 0;
              padding: 0;
              box-sizing: border-box;
            }
            body {
              background-image: url({INSERT YOUR IMAGE PATH FOR BACKGROUND});
              background-size: cover;
              background-repeat: no-repeat;
            }
        </style>
    </head>
    <body>

    </body>
</html>
```  
