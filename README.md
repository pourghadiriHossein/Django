# How to Load HTML File in Django

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


## Create urls.py file in homePage
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home')
]
```

## Write hello function for homePage views.py
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

## Simple HTML Template
```bash
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        *{
            font-size: 100px;
        }
    </style>
</head>
<body>
    <label for="likes" id="likes">0</label>
    <input type="button" value="👍" onclick="increse_likes()">
    <br>
    <label for="" id="galb">❤️</label>
    <script>
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        async function increse_likes(){
            var likes = document.getElementById("likes");
            n = parseInt(likes.innerHTML);
            console.log(n);
            likes.innerHTML = n+1;
            var size = document.getElementById('galb');
            for(var i=100; i<120; i++){
                size.style.fontSize = i+'px';
                await sleep (1)
            }
            for(var i=120; i>99; i--){
                size.style.fontSize = i+'px';
                await sleep (1)
            }
        }
    </script>
</body>
</html>
```

