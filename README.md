# Create Blog Project By Class View Structure

## Create Project without additional folder
```bash
django-admin startproject config .
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
                {% if user.is_authenticated %}
                <a class="nav-link" href="{% url 'create' %}">New Post</a>
                {% endif %}
            </div>
        </div>
        <div class="mx-1">
            {% if user.is_authenticated %}
                <span> Welcome {{ user.username }} </span> | <a href="{% url 'logout' %}" style="color: #222"> Logout </a>
            {% else %}
                <a href="{% url 'login' %}" style="color: #222">Login</a> | <a href="{% url 'signup' %}" style="color: #222"> Sign Up </a>
            {% endif %}
        </div>
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
## Create registration folder in root templates
- ### Create login.html file
```bash
{% extends '_base.html' %}

{% block title %}
    Login
{% endblock title %}

{% block content %}
    <div class="container p-5">
        <div class="card shadow p-5">
            <form action="" method="post">
                {% csrf_token %}
                <table>
                    {{ form.as_table }}
                </table>
                <input class="btn btn-success" type='submit' value='Login'>
            </form>
        </div>
    </div>
{% endblock content %}
```

- ### Create signup.html file
```bash
{% extends '_base.html' %}

{% block title %}
    Sign Up
{% endblock title %}

{% block content %}
    <div class="container p-5">
        <div class="card shadow p-5">
            <form action="" method="post">
                {% csrf_token %}
                <table>
                    {{ form.as_table }}
                </table>
                <input class="btn btn-success" type='submit' value='Sign Up'>
            </form>
        </div>
    </div>
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
    'blog',
    'accounts'
]
```
- ### Add Path to TEMPLATES DIR
```bash
str(BASE_DIR.joinpath('templates'))
```
- ### Add Login and Logout Redirect URL
```bash
LOGIN_REDIRECT_URL = 'posts_list'
LOGOUT_REDIRECT_URL = 'login'
```

## Update config\urls.py
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]
```

## accounts app
- ### Create urls.py file
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
```
- ### Create SignUpView function in views.py
```bash
from django.views import generic
from django.contrib.auth import forms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class SignUpView(generic.CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('posts_list'))

        return super().dispatch(request, *args, **kwargs)
```

## blog app
- ### Create templates folder 
- ### Create blog folder in templates folder
- ### Create posts_list.html file
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
                        {{ post.text | truncatewords:3 }}
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
- ### Create post_detail.html file
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
                {% if user.is_authenticated %}
                <div>
                    <a href = "{% url 'update' post.id %}" class="btn btn-sm btn-warning">Update</a>
                    <a href = "{% url 'delete' post.id %}" class="btn btn-sm btn-danger">Delete</a>
                </div>
                {% endif %}
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
- ### Create new_post.html file
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
                <form method="POST" action="{% url 'create' %}">
                    {% csrf_token %}
                    <table>
                        {{ form.as_table }}
                    </table>
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
- ### Create update_post.html file
```bash
{% extends '_base.html' %}

{% block title %}
Update Post
{% endblock title %}

{% block content %}

<div class="container mt-4">
    <div class="row">
        <div class="col-9">
            <div class="card shadow my-3 p-5">
                <h3>Update Post:</h3>
                <form method="POST" action="{% url 'update' post.id %}">
                    {% csrf_token %}
                    <table>
                        {{ form.as_table }}
                    </table>
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
- ### Create delete_post.html file
```bash
{% extends '_base.html' %}

{% block title %}
Delete Post
{% endblock title %}

{% block content %}

<div class='container'>
    <div class="card shadow my-5 mx-2 p-5">
        <h1>
            Delete Post?
        </h1>
        <p>
            Are You sure you want to delete post {{ post.title }} permanently?
        </p>
        <form method="POST" action="{% url 'delete' post.id %}">
            {% csrf_token %}
            <input class="btn btn-danger" type="submit" value="Yes, Delete.">
            <a class="btn btn-info" href="{% url 'post_detail' post.id %}">No, Back to Post Detail of post</a>
        </form>
    </div>
</div>

{% endblock content %}
```

- ### Update admin.py
```bash
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'datetime_created', 'datetime_modified', 'status']
    list_display_links = ['title', 'author', 'datetime_created', 'datetime_modified', 'status']
    ordering = ['status', 'author']
```

- ### Create forms.py file
```bash
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'status']
```

- ### Update models.py file
```bash
from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
```

- ### Create urls.py file
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view() , name='posts_list'),
    path('<int:pk>/', views.PostDetailView.as_view() , name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
]
```

- ### Update views.py file
```bash
from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' 

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/new_post.html'

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post 
    form_class = PostForm
    template_name = 'blog/update_post.html'
    login_url = 'login'

class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('posts_list')

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
