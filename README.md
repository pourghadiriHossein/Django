# Add Media and Pagination for Book Store Project

## config folder
- ### Update settings.py file - Add Media
```bash
# media files
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))
```
- ### Update urls.py file
```bash
from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', lambda request: render(request, "home.html" ), name='home'),
    path('', include('pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
## books app
- ### Update book_create.html in books Directory
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
افزودن کتاب
{% endblock page_title %}

{% block content %}
<div class="container mt-4" dir="rtl">
    <div class="row">
        <div class="col-9">
            <div class="card shadow my-3">
                <h5 class="card-header bg-success text-light px-5">فرم</h5>
                <div class="px-5 pt-3 pb-5">
                    <form method="POST" action="{% url 'book_create' %}" enctype="multipart/form-data">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <input class="btn btn-outline-success mt-3" type="submit" value="ایجاد کتاب">
                    </form>
                </div>
                
            </div>
        </div>
        <div class="col-3">
            <div class="card my-3 shadow">
                <h5 class="card-header bg-warning text-light">راهنما</h5>
                <div class="card-body">
                    <p class="card-text">
                        اطلاعات کتاب را در فرم این صفحه وارد کنید و سپس بر روی دکمه ذخیره کلیک کنید.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```
- ### Update book_detail.html file
```bash
{% extends '_base.html' %}

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
                        <h5 class="mb-3">ندا رحیمی</h5>
                        <p>با سلام چند تا نکته میخواستم بگم اول اینکه من جزء دسته از آدمایی بودم که میگفتم کتاب خوندن لذتش
                            به اینه که آدم کتابو بگیره دستش و بخونه اما واقعا میگم فیدیبو تو زمینه کاری خودش داره خوب عمل
                            میکنه امیدوارم روز به روز موفق تر بشه ممنون بابت کتابهای خوبی که میزارید چونکه خیلی به روزه</p>
                    </div>
                    <div class="border-bottom mb-3">
                        <h5 class="mb-3">هادی هاشمی</h5>
                        <p>با سلام چند تا نکته میخواستم بگم اول اینکه من جزء دسته از آدمایی بودم که میگفتم کتاب خوندن لذتش
                            به اینه که آدم کتابو بگیره دستش و بخونه اما واقعا میگم فیدیبو تو زمینه کاری خودش داره خوب عمل
                            میکنه امیدوارم روز به روز موفق تر بشه ممنون بابت کتابهای خوبی که میزارید چونکه خیلی به روزه</p>
                    </div>
                    <div>
                        <h5 class="mb-3">احمد چراغی </h5>
                        <p>با سلام چند تا نکته میخواستم بگم اول اینکه من جزء دسته از آدمایی بودم که میگفتم کتاب خوندن لذتش
                            به اینه که آدم کتابو بگیره دستش و بخونه اما واقعا میگم فیدیبو تو زمینه کاری خودش داره خوب عمل
                            میکنه امیدوارم روز به روز موفق تر بشه ممنون بابت کتابهای خوبی که میزارید چونکه خیلی به روزه</p>
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-center">
                <div class="card shadow my-3 p-5 w-sm-75 w-100">
                    <h3>نظر خود را وارد کنید:</h3>
                    <form method="POST">
                        <div class="form-group py-2">
                            <label class="py-1" for="author_name">نام شما:</label>
                            <input type="text" class="form-control" placeholder="نام خود را وارد کنید" name="author_name">
                        </div>
                        <div class="form-group py-2">
                            <label class="py-1" for="email">ایمیل شما:</label>
                            <input type="email" class="form-control" placeholder="example@gmail.com" name="email">
                        </div>
                        <div class="form-group py-2">
                            <label class="py-1" for="comment_text">متن نظر:</label>
                            <textarea class="form-control" name="text" rows="3"
                                      placeholder="نظر خود را اینجا وارد کنید"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">ارسال</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

- ### Update book_list.html file
```bash
{% extends '_base.html' %}

{% block page_title %}
لیست کتاب ها
{% endblock page_title %}

{% block content %}
<div class="container mt-4">
    <div class="row flex-row-reverse justify-content-md-start">
        {% for book in page_obj %}
            <div class="card m-2" style="max-width: 45%">
                <div class="row g-0 h-100" dir="rtl">
                    <div class="col-md-4">
                        {% if book.cover %}
                        <img src="{{ book.cover.url }}"
                            class="img-fluid rounded-start" alt="...">
                        {% endif %}
                    </div>
                    <div class="col-md-8 h-100">
                        <div class="d-flex flex-column justify-content-between h-100">
                            <div class="card-body">
                                <a class="text-decoration-none" href="{{ book.get_absolute_url }}">
                                    <h3 class="card-title"> 
                                        <strong>
                                            {{ book.title }}
                                        </strong>
                                    </h3>
                                </a>
                                <p class="card-text pt-3">{{ book.description|truncatewords:30 }}</p>
                                <p class="text-muted">نویسنده: {{ book.author }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
</div>
<nav aria-label="Page navigation example">
    <ul class="pagination mt-3 justify-content-center">
        {% if page_obj.has_previous %}
            <li class="page-item"><a class="page-link" href="{% url 'book_list'%}?page={{page_obj.previous_page_number}}">Previous</a></li>
        {% endif %}
      <li class="page-item"><a class="page-link" href="">{{ page_obj.number }}</a></li>
      {% if page_obj.has_next %}
          <li class="page-item"><a class="page-link" href="{% url 'book_list'%}?page={{page_obj.next_page_number}}">Next</a></li>
      {% endif %}
    </ul>
</nav>
<footer class="bg-light text-center text-lg-start mt-5">
  <div class="text-center bg-grey">
      <p>powered by : Poulstar</p>
  </div>
</footer>
{% endblock content %}
```
- ### Update book_update.html file
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
ویرایش کتاب {{ book.title }}
{% endblock page_title %}

{% block content %}
<div class="container mt-4" dir="rtl">
    <div class="row">
        <div class="col-9">
            <div class="card shadow my-3">
                <h5 class="card-header bg-success text-light px-5">فرم</h5>
                <div class="px-5 pt-3 pb-5">
                    <form method="POST" action="{% url 'book_update' book.id%}" enctype="multipart/form-data">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <input class="btn btn-outline-success mt-3" type="submit" value="ذخیره">
                    </form>
                </div>
            </div>
        </div>
        <div class="col-3">
            <div class="card my-3 shadow">
                <h5 class="card-header bg-warning text-light">راهنما</h5>
                <div class="card-body">
                    <p class="card-text">
                        اطلاعات کتاب را در فرم این صفحه وارد کنید و سپس بر روی دکمه ذخیره کلیک کنید.
                    </p>
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
```

- ### Update forms.py file
```bash
from django.forms import ModelForm
from . import models

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'author', 'description', 'price', 'cover']
```

- ### Update views.py file
```bash
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import BookForm
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
    context = {
        'book' : book
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
