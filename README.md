# Introduction

## <a href="https://www.djangoproject.com/">Django Web Site</a>

## <a href="https://docs.djangoproject.com/en/4.1/">Django documentation</a>

## <a href="https://www.djangoproject.com/download/">Django Installation</a>
```bash
pip install Django
```

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
### Create Project with additional folder
```bash
django-admin startproject myNewProject
```

### Create Project without additional folder
```bash
django-admin startproject myNewProject .
```

## Learn manage.py step by step
### In Windows
```bash
py manage.py
```

### In MacOS
```bash
python manage.py
```

### In Linux
```bash
python3 manage.py
```


## Create first app
### In Windows
```bash
py manage.py startapp myFirstApp
```

### In MacOS
```bash
python manage.py startapp myFirstApp
```

### In Linux
```bash
python3 manage.py startapp myFirstApp
```

## set new app in config\settings.py - insert 'myFristApp'

## Link myFirstApp in config\urls.py
```bash
from django.urls import include
```
```bash
add path('myFirstApp/', include('myFirstApp.urls'))
```


## Create urls.py file in myFirstApp
```bash
from django.urls import path
from . import views

urlpatterns = [
  path('hello/', views.hello, name='hello')
]
```

## Write hello function for myFirstApp views.py
```bash
from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse('Hello World')
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
