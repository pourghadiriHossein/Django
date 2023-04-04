# Create Book Store Project By Class Base Structure

## Create Project without additional folder
```bash
django-admin startproject config .
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

## Create static Folder
- ### <a href="https://github.com/pourghadiriHossein/Django/tree/session18">Download Template File and Copy css, fonts, icons folders to Static</a>

## Create Root templates Folder
- ### Create _base.html file
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
- ### Create registration Folder then Add This Files
- ### Create login.html file
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
- ### Create signup.html files
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Sign Up
{% endblock page_title %}

{% block content %}
<h1>
    Sign Up
</h1>
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success'>
        Sign Up
    </button>
</form>
<a class='btn btn-outline-warning mt-3' href="{% url 'login' %}">Login</a>
{% endblock content %}
```

- ### Create password_change_done.html File
```bash
{% extends '_base.html' %}

{% block page_title %}
Password Change Successful
{% endblock page_title %}

{% block content %}
<h1>
    Password Changed Successfully!
</h1>
{% endblock content %}
```

- ### Create password_change_form.html File
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Password Change
{% endblock page_title %}

{% block content %}
<form action="" method="POST" class="mt-3">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success mt-3'>
        Change
    </button>
</form>
{% endblock content %}
```

- ### Create password_reset_complete.html File
```bash
{% extends '_base.html' %}

{% block page_title %}
Successful Reset of Password
{% endblock page_title %}

{% block content %}
<h1>
    Reset Completed Successfully
</h1>
<p>
    Login And Enjoy
</p>
<p>
    You can login <a href="{% url 'login' %}">here</a>
</p>
{% endblock content %}
```

- ### Create password_reset_confirm.html File
```bash
{% extends '_base.html' %}

{% load crispy_forms_tags %}

{% block page_title %}
Set New Password
{% endblock page_title %}

{% block content %}
<form action="" method="POST">
    {% csrf_token %}
    <table>
        {{ form|crispy }}
    </table>
    <button type="submit" class='btn btn-outline-success mt-3'>
        Update Password
    </button>
</form>
{% endblock content %}
```

- ### Create password_reset_done.html File
```bash
{% extends '_base.html' %}

{% block page_title %}
Password Reset Done
{% endblock page_title %}

{% block content %}
<h1>
    Password Reset
</h1>
<h2>
    Email Sent
</h2>
<p>
    Check your email!
</p>
{% endblock content %}
```

- ### Create password_reset_email.html File
```bash
Hello, {{ user.username }}

Someone just asked for password reset of this email: {{ email }}

If it was you that asked for this link, please click on the link below:

{{ protocol }}://{{ domain }}{%url 'password_reset_confirm' uidb64=uid token=token %}

If you forgot your username: {{ user.username }}
Thanks for using our website.

Poulstar
```

- ### Create password_reset_form.html File
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

## config app
- ### Update settings.py File
```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'crispy_forms',
    'crispy_bootstrap5',
    'books',
]
```
```bash
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
```bash
STATIC_URL = 'static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
```
```bash
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "book_list"
LOGOUT_REDIRECT_URL = "book_list"
```
```bash
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
```bash
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```
```bash
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))
```

- ### Update urls.py File
```bash
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## accounts app
- ### Update models.py File
```bash
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
```
- ### Create forms.py File
```bash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age', )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
```
- ### Update admin.py File
```bash
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', )}),
    )

    list_display = ['username', 'email', 'age' , 'is_staff']
    list_display_links = ['username', 'email', 'age' , 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
```
- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SingUpView.as_view(), name='signup')
]
```
- ### Update views.py File
```bash
from django.views import generic
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

class SingUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
```
## books app
- ### Create templates Folder Then Create books Folder then Add This Files
- ### Create book_create.html File
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
- ### Create book_delete.html File
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
- ### Create book_detail.html File
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
                                 class="img-fluid rounded-start" alt="..." style="width: 210px;height: 260px;">
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
                        {% for comment in book.comments.all %}
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
- ### Create book_list.html File
```bash
{% extends '_base.html' %}

{% block page_title %}
لیست کتاب ها
{% endblock page_title %}

{% block content %}
<div class="container mt-4">
    <div class="row flex-row-reverse justify-content-md-start">
        {% for book in books %}
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
- ### Create book_update.html File
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
- ### Update models.py File
```bash
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Book(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
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
- ### Create forms.py File
```bash
from django.forms import ModelForm
from .models import Comment, Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "description", "price", "cover")

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields = ('text', 'recommend')
```
- ### Update admin.py File
```bash
from django.contrib import admin
from .models import Book, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'datetime_created', 'recommend', 'is_active')

admin.site.register(Book)
admin.site.register(Comment, CommentAdmin)
```
- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name="book_list"),
    path('<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('create/', views.BookCreateView.as_view(), name="book_create"),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name="book_update"),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name="book_delete"),
]
```
- ### Update views.py File
```bash
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book
from .forms import CommentForm, BookForm
from django.shortcuts import get_object_or_404, redirect

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = "books/book_list.html"
    context_object_name = "books"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    extra_context = {'book_form': CommentForm()}

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        if request.method=="POST":
            book_form = CommentForm(request.POST)
            if book_form.is_valid():
                new_comment = book_form.save(commit=False)
                new_comment.book = self.book
                new_comment.user = request.user
                new_comment.save()
                return redirect('book_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    template_name = "books/book_create.html"
    fields = ["title", "author", "description", "price", "cover"]
    success_url = reverse_lazy("book_list")

    def dispatch(self, request, *args, **kwargs):
        if request.method=="POST":
            book_form = BookForm(request.POST, request.FILES)
            if book_form.is_valid():
                new_book = book_form.save(commit=False)
                new_book.user = request.user
                new_book.save()
                return redirect('book_list')
        return super().dispatch(request, *args, **kwargs)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    template_name = "books/book_update.html"
    fields = ["title", "author", "description", "price", "cover"]

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = "books/book_delete.html"
    success_url = reverse_lazy("book_list")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
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