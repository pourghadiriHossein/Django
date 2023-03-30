# Add Comment Mechanism to Book Store Project

## books app
- ### Update book_detail.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
جزییات کتاب {{ book.title }}
{% endblock page_title %}

{% block content %}
<div class="container mt-5" dir="rtl">
    <div class="">
        <div class="">
            <div class="d-flex justify-content-center">
                <div class="row w-sm-75 w-100">
                    <div class="col-xs-12 col-md-3 d-flex justify-content-center">
                        <div>
                            {% if book.cover %}
                            <img class="shadow" src="{{ book.cover.url }}"
                                 class="img-fluid rounded-start" alt="...">
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-xs-12 col-md-6 text-center text-md-end mt-md-1 mt-4">
                        <h1>{{ book.title }}</h1>
                        <h5 class="small my-1"><span class="text-muted">نویسنده: </span>{{ book.author }}</h5>
                        <h5 class="small my-1"><span class="text-muted">مترجم: </span>الهام خرسندی</h5>
                        <h5 class="small my-1"><span class="text-muted">انتشارات: </span>هوزمزد</h5>
                    </div>
                    <div class="col-xs-12 col-md-3 d-flex flex-column">
                        <h3 class="align-self-center pt-2 text-muted align-self-md-end">
                            {{ book.price }} تومان
                        </h3>
                    </div>
                    <div class="col-xs-12 col-md-3 d-flex flex-column">
                        {% if user.is_authenticated %}
                        <a class="btn btn-outline-info" href="{% url 'book_update' book.pk %}">
                            ویرایش این کتاب
                        </a>
                        <a class="btn btn-outline-danger" href="{% url 'book_delete' book.pk %}">
                            حذف این کتاب
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-center">
                <div class="my-3 p-5 w-sm-75 w-100">
                    {{ book.description|linebreaks }}
                </div>
            </div>
            
            <div class="d-flex justify-content-center">
                <div class="card shadow my-3 p-5 w-sm-75 w-100">
                    <h2 class="mb-5">نظرات:</h2>
                    <div class="border-bottom mb-3">
                        {% for comment in comments %}
                            {% if comment.is_active %}
                                <h5 class="mb-3">
                                    {{ comment.user }} |
                                    {% if comment.recommend %}
                                        <span style="color: green;">
                                            این کتاب را توصیه میکنم.👍
                                        </span>
                                    {% else %}
                                        <span style="color: red;">
                                            این کتاب را توصیه نمیکنم.
                                        </span>
                                    {% endif %}
                                </h5>
                                    <p>
                                        {{ comment.text|linebreaks }}
                                    </p>
                                <hr>
                            {% endif %}
                        {% endfor %}
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-center">
                <div class="card shadow my-3 p-5 w-sm-75 w-100">
                    <h3>نظر خود را وارد کنید:</h3>
                    <form method="POST">
                        {% csrf_token %}
                        {% if user.is_authenticated %}
                          {{ comment_form|crispy }}
                        {% endif %}
                        <button type="submit" class="btn btn-primary mt-3">ارسال</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```



- ### Update models.py
```bash
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    author = models.CharField(max_length=100, verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='قیمت')
    cover = models.ImageField(upload_to="covers/", verbose_name='عکس جلد', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])
    
class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name="نام کتاب")
    text = models.TextField(verbose_name="متن پیام")
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    recommend = models.BooleanField(default=True, verbose_name="پیشنهاد می شود")

    def __str__(self):
        return f"{self.user}: {self.text}"
```
- ### Update admin.py file
```bash
from django.contrib import admin
from .models import Book, Comment

admin.site.register(Book)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'datetime_created', 'recommend', 'is_active')

admin.site.register(Comment, CommentAdmin)
```
- ### Update forms.py file
```bash
from django.forms import ModelForm
from . import models

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'author', 'description', 'price', 'cover']

class CommentForm(ModelForm):
    class Meta:
        model=models.Comment
        fields = ('text', 'recommend')
```

- ### Update views.py file
```bash
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import BookForm, CommentForm
from django.core.paginator import Paginator

def book_list_view(request):
    books = models.Book.objects.all()
    paginator = Paginator(books, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'books/book_list.html', context)

def book_detail_view(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    comments = book.comments.all()
    if request.method=="POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'books/book_detail.html', context)

def book_create_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        form = BookForm(request.POST,request.FILES)
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
        form = BookForm(request.POST, request.FILES, instance=book)
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
