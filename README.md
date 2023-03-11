# how to Use Media and SuperUser and Models and Test in Django Template

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
django-admin startproject myNewProject .
```

## Create app post
### In Windows
```bash
py manage.py startapp post
```
### In MacOS
```bash
python manage.py startapp post
```
### In Linux
```bash
python3 manage.py startapp post
```

## set new app in config\settings.py - insert 'post'

## Add Media Repository and Configuration in config\settings.py
```bash
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))
```

## Link post in config\urls.py
```bash
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Create templates Folder in homePage App
- ### Create index.html File


## Create urls.py file in post App
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```


## Write hello function for post views.py
```bash
from django.shortcuts import render

def index(request):
    posts = 0
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)
```

## Write Post Models Detail in post\models.py
```bash
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='upload')
    creator = models.CharField(max_length=40)
    create_at = models.DateTimeField()

    def __str__(self):
        return f"Post Title is: {self.title}"
```

## Add Admin Index Detail in post\admin.py
```bash
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

## Make Migrations for post app
- ### In Windows
```bash
py manage.py makemigrations post
```
- ### In MacOS
```bash
python manage.py makemigrations post
```
- ### In Linux
```bash
python3 manage.py makemigrations post
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


## load Static File Command In Django Template
```bash
{% load static %}
```


## How to Load Static File in href Or src In Django Template
```bash
{% static 'folder-name/file-name.extension' %}
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


## Add Three Post In Admin Panel

## Update index function for post App in views.py
```bash
from django.shortcuts import render

def index(request):
    posts = models.Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)
```

## Write new Class for post App in tests.py
```bash
from django.test import TestCase
from django.shortcuts import reverse
from .models import Post

class HarChiDostDari(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title = 'test',
            description = 'test aval',
            image = 'no image',
            creator = 'hossein',
            create_at = '2020-11-11 10:43',
        )

    def test_find_url(self): #Error
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_finding_url_by_name(self): #OK
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_finding_post_title_in_page(self): #OK
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.post.title)
        self.assertEqual(self.post.title, 'test')
```  
 
 
## Run Test in Django Project
- ### In Windows
```bash
py manage.py test
```
- ### In MacOS
```bash
python manage.py test
```
- ### In Linux
```bash
python3 manage.py test
```

## Simple HTML Template For Index
```bash
<!DOCTYPE html>
<html lang="en" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Your Web Page Title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark" id="nav">
        <div class="container-fluid">
            <a class="navbar-brand" href="javascript:void(0)">
                <img src="{Your Image Path}" alt="logo" width="40px">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
            <span class="navbar-toggler-icon"></span>
            </button>
        </div>
    </nav>
    <div class="container-sm mt-5">
        <div class="row gap-5 justify-content-center">
            <div class="col-lg-3 card">
                <img class="card-img-top" src="{Your Image Path}" alt="Card image cap" style="height:200px;">
                <div class="card-body">
                  <h5 class="card-title text-center">{ Post Title }</h5>
                  <p class="card-text text-center">{ Post Description }</p>
                </div>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">{ Post Creator }</li>
                <div class="card-body">
                  <span class="card-link">{ Post Create At }</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```
  
