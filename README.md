# Start Django Blog Project
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

## Create templates Folder in Root Directory
- ### Create _base.html File
```bash
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>{% block title %}{% endblock title %}</title>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-secondary">
    <div class="container-fluid mx-5 px-5">
        <a class="navbar-brand" href="https://www.poulstar.com" target="_blank">Poulstar.com</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <a class="nav-link active" aria-current="page" href="{% url 'posts_list' %}">Home</a>
                <a class="nav-link" href="{% url 'create' %}">New Post</a>
            </div>
        </div>
        <div class="mx-1">Welcome</div>
    </div>
</nav>

<div class="container-fluid bg-success">
    <div class="row py-3">
        <div class="col-md-8 col-md-10 mx-auto">
            <h3 class="my-4 mt-3 text-white">Welcome to Poulstar and Django course</h3>
            <p class="text-light">You will learn much about django here</p>
        </div>
    </div>
</div>

{% block content %}
{% endblock content %}

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

</body>
</html>
```

## Update TEMPLATES DIRS in config\settings.py
```bash
str(BASE_DIR.joinpath('templates'))
```

## Create app blog
### In Windows
```bash
py manage.py startapp blog
```
### In MacOS
```bash
python manage.py startapp blog
```
### In Linux
```bash
python3 manage.py startapp blog
```

## set new app in config\settings.py - insert 'blog'



## Link post in config\urls.py
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

## Create templates Folder in blog App
- ### Add blog Folder
- ### Create posts_list.html
```bash
{% extends '_base.html' %}

{% block title %}
Posts List
{% endblock title %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-9">
            {% for post in posts %}
            <div class="card shadow-sm my-3">
                <div class="card-body">
                    <h5 class="card-title"> {{ post.title }} </h5>
                    <h6 class="card-subtitle mb-2 text-muted small py-2"> {{ post.datetime_created }} </h6>
                    <p class="card-text py-3" style="text-align: justify;">
                    {{ post.text }}
                    </p>
                    <a href = "{% url 'post_detail' post.id %}" class="btn btn-sm btn-outline-success">Read More</a>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="col-3">
            <div class="card my-3 sticky-top">
                <h5 class="card-header">About</h5>
                <div class="card-body">
                    <p class="card-text";>Poulstar is an institute which help children learn
                        different programming languagess. Kids and teenager learn how to
                        code in different programming languages by games and playing.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```
- ### Create post_detail.html
```bash
{% extends '_base.html' %}

{% block title %}
post {{ post.title }} detail
{% endblock title %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-9">

            <div class="card shadow my-3 p-5">
                <h1>{{ post.title }}</h1>
                <p class="small text-muted mt-2">Created on: {{ post.datetime_created }}</p>
                <p class="mt-2" style="text-align: justify"> {{ post.text }}
                </p>
                <p class="small text-muted">Writer: {{ post.author }}</p>
                <p class="small text-muted mt">Last modified on: {{ post.datetime_modified }}</p>
            </div>
            
            <div class="card shadow my-3 p-5">
                <h3>Comments:</h3>
                Comments will be shown here ...
            </div>
        
            <div class="card shadow my-3 p-5">
                <h3>Add new comment:</h3>
                <form method="POST">
                    <div class="form-group py-2">
                        <label class="py-1" for="author_name">Enter your name:</label>
                        <input type="text" class="form-control" placeholder="e.g. John Doe" name="author_name">
                    </div>
                    <div class="form-group py-2">
                        <label class="py-1" for="email">Your Email:</label>
                        <input type="email" class="form-control" placeholder="example@gmail.com" name="email">
                    </div>
                    <div class="form-group py-2">
                        <label class="py-1" for="comment_text">Comment text:</label>
                        <textarea class="form-control" name="text" rows="3" placeholder="Enter your comment text here..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary mt-1">Submit</button>
                </form>
            </div>
        </div>
        <div class="col-3">
            <div class="card my-3 sticky-top">
                <h5 class="card-header">About</h5>
                <div class="card-body">
                    <p class="card-text";>Poulstar is an institute which help children learn
                        different programming languagess. Kids and teenager learn how to
                        code in different programming languages by games and playing.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```
- ### Create new_post.html
```bash
{% extends '_base.html' %}

{% block title %}
Create New Post
{% endblock title %}

{% block content %}

<div class="container mt-4">
    <div class="row">
        <div class="col-9">
            <div class="card shadow my-3 p-5">
                <h3>Add new Post:</h3>
                <form method="POST">
                    <div class="form-group py-2">
                        <label class="py-1">Enter post title</label>
                        <input type="text" class="form-control" placeholder="e.g. Some Title" name="title">
                    </div>
                    <div class="form-group py-2">
                        <label class="py-1">Enter post text:</label>
                        <textarea class="form-control" name="text" rows="8" placeholder="Enter your post text here..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
        <div class="col-3">
            <div class="card my-3 sticky-top">
                <h5 class="card-header">About</h5>
                <div class="card-body">
                    <p class="card-text";>Poulstar is an institute which help children learn
                        different programming languagess. Kids and teenager learn how to
                        code in different programming languages by games and playing.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

{% endblock content %}
```

## Write blog Models Detail in blog\models.py
```bash
from django.db import models


class Post(models.Model):
    STATUS_CHOICES = (
        ('pub', 'published'),
        ('drf', 'draft'),
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=3)

    def __str__(self):
        return self.title
```

## Add Admin Index Detail in blog\admin.py
```bash
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'datetime_created', 'datetime_modified', 'status']
    list_display_links = ['title', 'author', 'datetime_created', 'datetime_modified', 'status']
    ordering = ['status', 'author']
```


## Create urls.py file in blog App
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_view, name='posts_list'),
    path('<int:pk>/', views.post_detail_view, name='post_detail'),
    path('create/', views.post_create_view, name='create'),
]
```


## Write function for blog views.py
```bash
from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post_list_view(request):
    posts = Post.objects.filter(status='pub')
    context = { 'posts': posts }
    return render(request, 'blog/posts_list.html', context)

def post_detail_view(request, pk):
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(Post, pk=pk)
    context = { 'post': post }
    return render(request, 'blog/post_detail.html', context)

def post_create_view(request):
    return render(request, 'blog/new_post.html')
```



## Make Migrations for blog app
- ### In Windows
```bash
py manage.py makemigrations blog
```
- ### In MacOS
```bash
python manage.py makemigrations blog
```
- ### In Linux
```bash
python3 manage.py makemigrations blog
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
