# Add Book Object in Book Store Project

## Create app books
### In Windows
```bash
py manage.py startapp books
```
### In MacOS
```bash
python manage.py startapp books
```
### In Linux
```bash
python3 manage.py startapp books
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
    'books',
]
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
    path('books/', include('books.urls')),
]
```

## books app
- ### Create templates Folder then Create books Directory
- ### Create book_list.html in books Directory
```bash
{% extends '_base.html' %}

{% block page_title %}
لیست کتاب ها
{% endblock page_title %}

{% block content %}
    {% for book in books %}
        <h1>
            {% comment %} <a href="{% url 'book_detail' book.pk %}"> {% endcomment %}
            <a href="{{ book.get_absolute_url }}">
                {{ book.title }}
            </a>
        </h1>
        <p>
            {{ book.description }}
        </p>
        {% endfor %}
{% endblock content %}
```
- ### Create book_datail.html in books Directory
```bash
{% extends '_base.html' %}

{% block page_title %}
جزییات کتاب {{ book.title }}
{% endblock page_title %}

{% block content %}
    <h1>
        {{ book.title }}
    </h1>
    <p>
        {{ book.description }}
    </p>
    <p>
        {{ book.author }}
    </p>
    <h4>
        {{ book.price }}
    </h4>
    <br>
    <a href="{% url 'book_list' %}">
        لیست همه کتاب ها
    </a>
{% endblock content %}
```

- ### Update models.py file
```bash
from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])
```

- ### Update admin.py file
```bash
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

- ### Create urls.py file
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_view, name="book_list"),
    path('<int:pk>/', views.book_detail_view, name="book_detail"),
]
```
- ### Update views.py file
```bash
from django.shortcuts import render, get_object_or_404
from . import models

def book_list_view(request):
    books = models.Book.objects.all()
    context = {
        'books' : books
    }
    return render(request, 'books/book_list.html', context)

def book_detail_view(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    context = {
        'book' : book
    }
    return render(request, 'books/book_detail.html', context)
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
