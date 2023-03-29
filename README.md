# Use Template File for Book Store Project

## Create static Folder in root Directory
- ### Move css, fonts, icons Folder to static

## Update root templates
- ### Update _base.html file
```bash
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block page_title %}{% endblock page_title %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block styles %}
    {% endblock styles %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-info" dir="rtl">
        <div class="container">
            <a class="navbar-brand">
                <img src="{% static 'icons/book.png' %}" alt="icon" height="30"
                     class="d-inline-block align-text-top">
            </a>
            <a class="navbar-brand mx-3">کتاب یار</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                    aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-link active" aria-current="page" href="{% url 'book_list' %}">خانه</a>
                    <a class="nav-link" href="{% url 'book_create' %}">اضافه کردن کتاب</a>
                </div>
            </div>
            {% if user.is_authenticated %}
                <div class="mx-2 text-white"> خوش آمدید  {{ user.username }}
                <span style="margin: 0 10px;">|</span>
                <a class="link-light text-decoration-none" href="{% url 'logout' %}">خروج</a></div>
            {% else %}
                <div class="link-light text-decoration-none">
                    <a class="link-light text-decoration-none" href="{% url 'login' %}"> ورود </a>
                    <span style="margin: 0 10px;">|</span>
                    <a class="link-light text-decoration-none" href="{% url 'signup' %}"> ثبت نام </a>
                </div>
            {% endif %}
        </div>
    </nav>   
    <div class='container mt-5'>
        {% block content %}
        {% endblock content %}
    </div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
</body>
</html>
```
- ### Update registration\login.html file
```bash
{% extends '_base.html' %}

{% load static %}
{% load crispy_forms_tags %}

{% block page_title %}
Login
{% endblock page_title %}
{% block styles %}
    <link rel="stylesheet" href="{% static 'css/login.css' %}">
{% endblock styles %}

{% block content %}
<div class="d-flex justify-content-center mt-5" dir="rtl">
    <div class="col-xl-3 col-lg-4 col-md-5 col-sm-5 col-xs-6 bg-white m-3 m-sm-5 border rounded px-4 pt-4 pb-3 shadow">
        <form method="post">
            {% csrf_token %}
            <h1 class="text-center">ورود</h1>
            {{ form|crispy }}
            <div class="d-flex justify-content-between align-items-center">
                <div class="mt-2">
                    <a class="text-decoration-none" href="{% url 'password_reset' %}">فراموشی رمز عبور</a>
                </div>
            </div>
            <button type="submit" class="btn btn-success mt-3 w-100">ورود</button>
            <div class="line-with-middle-sep">
                  <span>
                    یا
                  </span>
            </div>
            <a href="{% url 'signup' %}" class="btn btn-primary mt-2 mb-3 w-100">ثبت نام</a>
        </form>
    </div>
</div>
{% endblock content %}

```
- ### Update registration\password_reset_form.html file
```bash
{% extends '_base.html' %}

{% load static %}
{% load crispy_forms_tags %}

{% block page_title %}
Password Reset
{% endblock page_title %}
{% block styles %}
    <link rel="stylesheet" href="{% static 'css/login.css' %}">
{% endblock styles %}

{% block content %}
<div class="d-flex justify-content-center mt-5" dir="rtl">
    <div class="col-xl-3 col-lg-4 col-md-5 col-sm-5 col-xs-6 bg-white m-3 m-sm-5 border rounded px-4 pt-4 pb-3 shadow">
        <form method="post">
            {% csrf_token %}
            <h3 class="text-center">بازیابی رمز عبور</h3>
            {{ form|crispy }}
            <button type="submit" class="btn btn-success mt-3 w-100">ارسال</button>
            <div class="d-flex justify-content-between align-items-center">
                <div class="mt-2">
                    <a class="text-decoration-none" href="{% url 'login' %}">ورود</a>
                        یا
                    <a class="text-decoration-none" href="{% url 'signup' %}">ثبت نام</a>
                </div>
            </div>
        </form>
    </div>
</div>
{% endblock content %}

```

## pages app
- ### Update views.py file
```bash
from django.shortcuts import render, redirect

def home_page_view(request):
    return redirect('book_list')
```

## config folder
- ### Update settings.py file - Add STATICFILES_DIRS
```bash
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
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
                    <form method="POST" action="{% url 'book_create' %}">
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
                            <img src="https://newcdn.fidibo.com/images/books/65579_50411_normal.jpg"
                                 class="img-fluid rounded-start" alt="...">
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
    <div class="row flex-row-reverse justify-content-md-center">
        {% for book in books %}
            <div class="card m-2" style="max-width: 45%">
                <div class="row g-0 h-100" dir="rtl">
                    <div class="col-md-4">
                        <img src="https://newcdn.fidibo.com/images/books/69249_94233_normal.jpg"
                            class="img-fluid rounded-start" alt="...">
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

<footer class="bg-light text-center text-lg-start mt-5">
  <div class="text-center bg-grey">
      <p>powered by : Poulstar</p>
  </div>
</footer>
{% endblock content %}
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
