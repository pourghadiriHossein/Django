# Add Create and Update and Delete to books app in Book Store Project

## books app
- ### Update book_datail.html in books Directory
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
    {% if user.is_authenticated %}
    <br>
    <a class="btn btn-outline-info" href="{% url 'book_update' book.pk %}">
        ویرایش این کتاب
    </a>
    <a class="btn btn-outline-danger" href="{% url 'book_delete' book.pk %}">
        حذف این کتاب
    </a>
    {% endif %}
    <br>
    <a href="{% url 'book_list' %}">
        لیست همه کتاب ها
    </a>
{% endblock content %}

```
- ### Create book_create.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
افزودن کتاب
{% endblock page_title %}

{% block content %}
<form method="POST" action="{% url 'book_create' %}">
    {% csrf_token %}
    {{ form|crispy }}
    <input class="btn btn-outline-success mt-3" type="submit" value="ایجاد کتاب">
</form>
{% endblock content %}
```

- ### Create book_update.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
ویرایش کتاب {{ book.title }}
{% endblock page_title %}

{% block content %}
<form method="POST" action="{% url 'book_update' book.id%}">
    {% csrf_token %}
    {{ form|crispy }}
    <input class="btn btn-outline-success mt-3" type="submit" value="ذخیره">
</form>
{% endblock content %}
```

- ### Create book_delete.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
حذف کتاب {{ book.title }}
{% endblock page_title %}

{% block content %}
<form method="POST" action="{% url 'book_delete' book.id %}">
    {% csrf_token %}
    <h1>
        حذف کتاب {{ book.title }}
    </h1>
    <p>
        آیا از حذف کتاب {{ book.title }} مطمئن هستید؟
    </p>
    <input class="btn btn-outline-danger mt-3" type="submit" value="بله حذف شود.">
    <a class="btn btn-outline-secondary mt-3" href="{% url 'book_detail' book.id %}">خیر. به صفحه قبل برگرد.</a>
</form>
{% endblock content %}
```
- ### Create forms.py file
```bash
from django.forms import ModelForm
from . import models

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'author', 'description', 'price']
```

- ### Create urls.py file
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_view, name="book_list"),
    path('<int:pk>/', views.book_detail_view, name="book_detail"),
    path('create/', views.book_create_view, name="book_create"),
    path('<int:pk>/update/', views.book_update_view, name="book_update"),
    path('<int:pk>/delete/', views.book_delete_view, name="book_delete"),
]
```
- ### Update views.py file
```bash
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import BookForm

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

def book_create_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_create.html', { 'form': form } )

def book_update_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('book_list')
    book = get_object_or_404(models.Book, pk=pk)
    if request.method == 'GET':
        form = BookForm(instance=book)
        return render(request, 'books/book_update.html', { 'form': form , 'book': book})
    elif request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')

def book_delete_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    book = get_object_or_404(models.Book, pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', { 'book': book })  
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
