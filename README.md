# Start Shop Project

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

## Create app shop
### In Windows
```bash
py manage.py startapp shop
```
### In MacOS
```bash
python manage.py startapp shop
```
### In Linux
```bash
python3 manage.py startapp shop
```

## Create static Folder 
- ### Add CSS, FONT, IMAGE, JS Folder From Session24 to This Directory 

## Create Templates Folder in Root Directory
- ### Create publicLayout.html File
```bash
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="developed for Poulstar HTML, CSS, JS, education">
    <meta name="keywords" content="HTML, CSS, JavaScript">
    <meta name="author" content="Poulstar">
    <title>فروشگاه پل استار</title>
    <link rel="shortcut icon" href="{% static 'IMAGE/logo/TopBarLogo.png' %}" type="image/x-icon">
    <link rel="stylesheet" href="{% static 'CSS/Main.css' %}">
    
    {% block css %}{% endblock %}
    
</head>
<body>
    <button onclick="topFunction()" id="myBtn" title="Go to top">&uArr;</button>
    <div class="mainBox topHeader">
        {% if not user.is_authenticated  %}
        <a class="link" href="{% url 'login' %}"><button class="inlineLogin {% if urlName == 'login' %} active {%endif%}">ورود</button></a>
        <a class="link" href="{% url 'sign_up' %}"><button class="inlineLogin {% if urlName == 'sign_up' %} active {%endif%}">ثبت نام</button></a>
        {% else %}
        <a class="link" href="{% url 'dashboard' %}"><button class="inlineLogin {% if urlName == 'dashboard' %} active {%endif%}">داشبورد</button></a>
        <a class="link" href="{% url 'logout' %}"><button class="inlineLogin {% if urlName == 'logout' %} active {%endif%}">خروج</button></a>
        {% endif %}
        <p id="customizeDate" class="inlineDate"></p>
    </div>
    <div class="mainBox topBarLogo">
        <img src="{% static 'IMAGE/logo/TopBarLogo.png' %}" alt="TopBarLogo">
    </div>
    <div class="mainBox menu">
        <ul>
            <a class="linkMenu" href="{% url 'home' %}"><li class=" {% if urlName == 'home' %} active {%endif%}">خانه</li></a>
            {% for category in categories %}
            <li class="dropdown">
                <button class="dropbtn {% if urlName == 'product' %} active {%endif%}"><a href="{% url 'product' category.id %}">{{ category.label }}</a></button>
                <div class="dropdown-content">
                    {% for sub in category.categories.all %}
                    <a class="linkMenu" href="{% url 'product' sub.id %}"> {{ sub.label }}</a>
                    {% endfor %}
                </div>
            </li>
            {% endfor %}
            <a class="linkMenu" href="{% url 'contact' %}"><li class="{% if urlName == 'contact' %} active {%endif%}">تماس با ما</li></a>
            <a class="linkMenu" href="{% url 'faq' %}"><li class="{% if urlName == 'faq' %} active {%endif%}">سوالات متداول</li></a>
            <a class="linkMenu" href="{% url 'tac' %}"><li class="{% if urlName == 'tac' %} active {%endif%}">قوانین و مقررات</li></a>
            <li class="ShopingCartLogo dropdown">
                <span class="ShopingCartCounter center dropbtn">3</span>
                <div class="dropdown-content">
                    <a class="btn" href="{% url 'cart' %}">فاکتور کن</a>
                    <a class="linkMenu" href="{% url 'singleProduct' 1 %}">
                        <img class="cart" src="{% static 'IMAGE/product/dress1-1-700x893.jpg' %}" alt="dress1-1">
                        <div class="box">
                            <div class="detail">
                                <span>لباس مجلسی</span>
                                <del>700000 ريال</del>
                                <ins> 600000 ريال</ins>
                                <span>تعداد: 1</span>
                                <ins> 600000 ريال</ins>
                            </div>
                        </div>
                    </a>
                    <a class="linkMenu" href="{% url 'singleProduct' 2 %}">
                        <img class="cart" src="{% static 'IMAGE/product/hoodie1-1-700x893.jpg' %}" alt="hoodie1-1">
                        <div class="box">
                            <div class="detail">
                                <span>هودی</span>
                                <del>700000 ريال</del>
                                <ins> 600000 ريال</ins>
                                <span>تعداد: 2</span>
                                <ins> 1200000 ريال</ins>
                            </div>
                        </div>
                    </a>
                    <a class="linkMenu" href="{% url 'singleProduct' 3 %}">
                        <img class="cart" src="{% static 'IMAGE/product/jeans1-1-700x893.jpg' %}" alt="jeans1-1">
                        <div class="box">
                            <div class="detail">
                                <span>شلوار لی</span>
                                <del>500000 ريال</del>
                                <ins> 400000 ريال</ins>
                                <span>تعداد: 3</span>
                                <ins> 1200000 ريال</ins>
                            </div>
                        </div>
                    </a>
                </div>
            </li>            
        </ul>
    </div>
    <div class="whiteSpace"></div>
    {% block content %}{% endblock %}
    <div class="whiteSpace"></div>
    <div class="mainBox footer">
        <div class="box">
            <label class="footerFont" for="contact">تماس با ما</label>
            <p>شماره تماس: 34911-013</p>
            <p>آدرس: گیلان - رشت - گلسار - چهار راه اصفهان</p>
            <p>پست الکترونیک: info@poulstar.com</p>
        </div>
        <div class="box">
            <label class="footerFont" for="about">درباره ما</label>
            <p>
                سایت آموزشی فروشگاه آنلاین صرفا جهت آموزش بوده و استفاده از آن بلا مانع است.
            </p>
        </div>
        <div class="box">
            <label class="footerFont" for="tag">تگ</label>
            {% for tag in tags %}
            <button class="footerBTN"><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></button>
            {% endfor %}
        </div>
        <div class="box">
            <label class="footerFont" for="payment">پرداخت</label>
            <p>کلیه تراکنش های موجود در این سایت از طریق ID Pay صورت می گیرد و به صورت آزمایشی می باشد.</p>
        </div>
    </div>
    <script src="{% static 'JS/Layout.js' %}"></script>
    {% block js %}{% endblock %}
</body>
</html>
```

- ### Create registration in Root Templates Folder For Login and Signup
- ### Create Login.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Login.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox login">
    <h1>ورود</h1>
    <hr>
    <div class="loginBox">
        <form action="" method="" autocomplete="on">
            <input type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
            <input type="password" name="password" placeholder="رمز عبور خود را وارد کنید">
            <input type="submit" value="ارسال کن">
        </form>
    </div>
    <div class="guideBox">
        <p>فرم آزمایشی پروژه پل استار جهت آموزش بهتر و کاردبری تر با ضاهر مناسب جهت ارتباط گیری بیشتر با مبحث تحصیلی می باشد</p>
        <p>شماره تماس: 34911-013</p>
        <p>آدرس: گیلان - رشت - گلسار - چهار راه اصفهان</p>
        <p>پست الکترونیک: info@poulstar.com</p>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```

- ### Create signup.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Register.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox register">
    <h1>ثبت نام</h1>
    <hr>
    <div class="registerBox">
        <form action="" method="" autocomplete="on">
            <input type="text" name="name" placeholder="نام و نام خانوادگی خود را وارد کنید">
            <input type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
            <input type="text" name="email" placeholder="پست الکترونیک خود را وارد کنید">
            <input type="password" name="password" placeholder="رمز عبور خود را وارد کنید">
            <input type="submit" value="ارسال کن">
        </form>
    </div>
    <div class="guideBox">
        <p>فرم آزمایشی پروژه پل استار جهت آموزش بهتر و کاردبری تر با ضاهر مناسب جهت ارتباط گیری بیشتر با مبحث تحصیلی می باشد</p>
        <p>شماره تماس: 34911-013</p>
        <p>آدرس: گیلان - رشت - گلسار - چهار راه اصفهان</p>
        <p>پست الکترونیک: info@poulstar.com</p>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```

## config Side
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
    'shop',
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
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))
```
```bash
AUTH_USER_MODEL = "accounts.CustomUser"
```
- ### Update urls.py File
```bash
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
## accounts app
- ### Update models.py File
```bash
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=14, unique=True, null=True, blank=True)
    status = models.SmallIntegerField(default=1)
```
- ### Create forms.py File
```bash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('phone', 'status')

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
        (None, {'fields': ('phone', 'status' )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'status' )}),
    )

    list_display = ['username', 'email', 'phone', 'status' , 'is_staff']
    list_display_links = ['username', 'email', 'phone', 'status' , 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
```
- ### Update views.py File
```bash
from django.shortcuts import render
from django.urls import resolve
from shop import models

def login(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'registration/login.html', context)

def sign_up(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'registration/signup.html', context)

def logout(request):
    return True
```
- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),
]
```
## shop app
- ### Create templatetags Folder
- ### Creata __init__.py File
- ### Create tools.py File
```bash
from django import template
register = template.Library()


@register.filter()
def showPrice(value):
    return int(value)
@register.filter()
def mines(value, arg):
    exe = value - arg
    return int(exe)
@register.filter()
def calculateDiscount(value, arg):
    deprice = value*arg/100
    new_price = value-deprice
    return int(new_price)
```

- ### Create templates Folder
- ### In templates Folder, Create dashboard Folder
- ### In dashboard Folder, Create dashboard.html File
```bash
{% load static %}
{% load tools %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Poulstar</title>
    <link rel="stylesheet" href="{% static '/CSS/Dashboard.css' %}">
    <script src="{% static '/JS/Dashboard.js' %}" defer></script>
</head>
<body>
    

    <div class="right-side-menu">
        <div class="menu-title">
            <p class="p-white">داشبورد</p>
        </div>
        <div class="section">
            <ul class="menu-list">
                <li class="list-item">
                    <button class="list-btn">پروفایل</button>
                    <div class="items">
                        <a class="a-style item" onclick="showContent('content-profile')">اطلاعات شخصی</a>
                    </div>
                </li>
                <li class="list-item">
                    <button class="list-btn">آدرس ها</button>
                    <div class="items">
                        <a class="a-style item" onclick="showContent('content-address')">لیست آدرس</a>
                    </div>
                </li>
                <li class="list-item">
                    <button class="list-btn">نظر ها</button>
                    <div class="items">
                        <a class="a-style item" onclick="showContent('content-comment')">لیست نظر</a>
                    </div>
                </li>
                <li class="list-item">
                    <button class="list-btn">فاکتور ها</button>
                    <div class="items">
                        <a class="a-style item" onclick="showContent('content-order')">لیست فاکتور</a>
                    </div>
                </li>
                <li class="list-item">
                    <button class="list-btn">تراکنش ها</button>
                    <div class="items">
                        <a class="a-style item" onclick="showContent('content-transaction')">لیست تراکنش</a>
                    </div>
                </li>
            </ul>
        </div>
    </div>
    <div class="top-nav">
        <div class="top-nav-bar">
            <ul class="ul-style">
                <a class="a-style" href="{% url 'home' %}"><li class="li-style">صفحه اصلی</li></a>
                <a class="a-style" href="{% url 'logout' %}"><li class="li-style">خروج</li></a>
            </ul>
        </div>
        <div class="top-nav-title">
            <p class="p-white">
                {% if user.is_authenticated %}
                {{ user }}
                {% endif %}
            </p>
        </div>
    </div>
    <div class="content-base">

        <div id="content-profile" class="content-hidden-start" data-type="content">
            <div class="visit-part">
                <div class="image-box">
                    <img src="{% static '/IMAGE/avatar/avatar.png' %}" alt="avatar">
                </div>
                <div class="data-part">
                    <table>
                        <tr>
                            <th class="first">نام کاربری</th>
                            <th class="second">حسین پورقدیری</th>
                        </tr>
                        <tr>
                            <th class="first">شماره تماس</th>
                            <th class="second">09398932183</th>
                        </tr>
                        <tr>
                            <th class="first">پست الکترونیک</th>
                            <th class="second">hossein.654321@yahoo.com</th>
                        </tr>
                        <tr>
                            <th colspan="2">
                                <button class="update-profile" onclick="openDialogBox('profile-dialog-box')">ویرایش</button>
                            </th>
                        </tr>
                    </table>
                </div>
                <div class="profile-dialog-box" id="profile-dialog-box">
                    <div class="close-box" onclick="closeDialogBox('profile-dialog-box')">&#x2715;</div>
                    <div class="profile-dialog-box-content">
                        <form action="" autocomplete="on" method="post">
                            <input type="text" name="username" placeholder="نام کاربری خود را وارد کنید">
                            <input type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
                            <input type="text" name="email" placeholder="پست الکترونیک خود را وارد کنید">
                            <input type="submit" value="ارسال کن">
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <div id="content-address" class="content-hidden-start" data-type="content">
            <div class="visit-part">
                <table class="address">
                    <thead>
                        <tr>
                            <th>شناسه</th>
                            <th>استان</th>
                            <th>شهر</th>
                            <th>جزئیات آدرس</th>
                            <th colspan="2">امکانات</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                         <tr>
                            <td>1</td>
                            <td>گیلان</td>
                            <td>رشت</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-1')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <form action="post-for-update/1" autocomplete="on" method="post">
                                        <input list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            <option value="1">گیلان</option>
                                            <option value="2">تهران</option>
                                            <option value="3">خراسان</option>
                                            <option value="4">ایلام</option>
                                        </datalist>
                                        <input list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            <option value="1">رشت</option>
                                            <option value="2">انزلی</option>
                                            <option value="3">رودسر</option>
                                            <option value="4">لاهیجان</option>
                                        </datalist>
                                        <input type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div id="content-comment" class="content-hidden-start" data-type="content">
            <div class="visit-part">
                <table class="address">
                    <thead>
                        <tr>
                            <th>شناسه</th>
                            <th>نام محصول</th>
                            <th>نظر ارائه شده</th>
                            <th>وضعیت</th>
                            <th>امکانات</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>لباس مجلسی</td>
                            <td>لباس بسیار مرغوب و عالی</td>
                            <td>
                                <button class="table-btn success">فعال</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('comment-dialog-box-delete-1')">حذف</button>
                            </td>
                            <div class="comment-dialog-box-delete" id="comment-dialog-box-delete-1">
                                <div class="close-box" onclick="closeDialogBox('comment-dialog-box-delete-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>نظر مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن نظر مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/1" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('comment-dialog-box-delete-1')">خیر</a>
                                </div>
                            </div>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>لباس مجلسی</td>
                            <td>لباس بسیار مرغوب و عالی</td>
                            <td>
                                <button class="table-btn danger">غیر فعال</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('comment-dialog-box-delete-2')">حذف</button>
                            </td>
                            <div class="comment-dialog-box-delete" id="comment-dialog-box-delete-2">
                                <div class="close-box" onclick="closeDialogBox('comment-dialog-box-delete-2')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>ظر مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن نظر مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="delete/2" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('comment-dialog-box-delete-2')">خیر</a>
                                </div>
                            </div>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div id="content-order" class="content-hidden-start" data-type="content">
            <div class="visit-part">
                <table class="address">
                    <thead>
                        <tr>
                            <th>شناسه</th>
                            <th>جزئیات آدرس</th>
                            <th>کد تخفیف</th>
                            <th>مبلغ کل</th>
                            <th>مبلغ پرداختی</th>
                            <th>لیست خرید</th>
                            <th>وضعیت</th>
                            <th>امکانات</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>Gift_code</td>
                            <td>500000 ريال</td>
                            <td>400000 ريال</td>
                            <td>
                                <button class="table-btn info" onclick="openDialogBox('order-dialog-box-detail-1')">محصولات</button>
                            </td>
                            <td>
                                <button class="table-btn success">فعال</button>
                            </td>
                            <td>
                                <button class="table-btn success">پرداخت شده</button>
                            </td>
                            <div class="order-dialog-box-update" id="order-dialog-box-detail-1">
                                <div class="close-box" onclick="closeDialogBox('order-dialog-box-detail-1')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <div class="product-title">
                                        <span class="product-title-item" style="width: 10%;">شناسه</span>
                                        <span class="product-title-item" style="width: 20%;">نام محصول</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ اصلی</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ با تخفیف</span>
                                        <span class="product-title-item" style="width: 10%;">تعداد</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ پرداخت شده</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">1</span>
                                        <span class="product-body-item" style="width: 20%;">کیف</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">400000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">1</span>
                                        <span class="product-body-item" style="width: 20%;">400000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>  
                                </div>
                            </div>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>گلسار- چهار راه دیلمان اصفهان</td>
                            <td>Gift_code</td>
                            <td>500000 ريال</td>
                            <td>400000 ريال</td>
                            <td>
                                <button class="table-btn info" onclick="openDialogBox('order-dialog-box-detail-2')">محصولات</button>
                            </td>
                            <td>
                                <button class="table-btn danger">غیر فعال</button>
                            </td>
                            <td>
                                <button class="table-btn danger"><a href="peyment/2" class="a-style">پرداخت</a></button>
                            </td>
                            <div class="order-dialog-box-update" id="order-dialog-box-detail-2">
                                <div class="close-box" onclick="closeDialogBox('order-dialog-box-detail-2')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <div class="product-title">
                                        <span class="product-title-item" style="width: 10%;">شناسه</span>
                                        <span class="product-title-item" style="width: 20%;">نام محصول</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ اصلی</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ با تخفیف</span>
                                        <span class="product-title-item" style="width: 10%;">تعداد</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ پرداخت شده</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">1</span>
                                        <span class="product-body-item" style="width: 20%;">کیف</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">400000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">1</span>
                                        <span class="product-body-item" style="width: 20%;">400000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">لباس</span>
                                        <span class="product-body-item" style="width: 20%;">600000 ريال</span>
                                        <span class="product-body-item" style="width: 20%;">500000 ريال</span>
                                        <span class="product-body-item" style="width: 10%;">2</span>
                                        <span class="product-body-item" style="width: 20%;">1000000 ريال</span>
                                    </div>  
                                </div>
                            </div>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div id="content-transaction" class="content-hidden-start" data-type="content">
            <div class="visit-part">
                <table class="address">
                    <thead>
                        <tr>
                            <th>شناسه</th>
                            <th>شناسه فاکتور</th>
                            <th>مبلغ پرداخت شده</th>
                            <th>کد رهگیری</th>
                            <th>شناسه رهگیری</th>
                            <th>شماره کارت</th>
                            <th>تاریخ پرداخت</th>
                            <th>تاریخ تایید پرداخت</th>
                            <th>وضعیت</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>2</td>
                            <td>4500000 ريال</td>
                            <td>vdhvkdf9473f79dhukv7</td>
                            <td>4836346</td>
                            <td style="direction: ltr;">5892-****-****-1604</td>
                            <td style="direction: ltr;">1401/05/10 14:30:43</td>
                            <td style="direction: ltr;">1401/05/10 14:30:58</td>
                            <td>
                                <button class="table-btn success">موفق</button>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>4</td>
                            <td>4500000 ريال</td>
                            <td>vdhvkdf9473f79dhukv7</td>
                            <td>4836346</td>
                            <td style="direction: ltr;">5892-****-****-1604</td>
                            <td style="direction: ltr;">1401/05/10 14:30:43</td>
                            <td style="direction: ltr;">1401/05/10 14:30:58</td>
                            <td>
                                <button class="table-btn danger">ناموفق</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>

</body>
</html>
```
- ### In templates Folder, Create public Folder
- ### In public Folder, Create cart.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Cart.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox finalCart">
    <h1>سبد خرید</h1>
    <table>
        <thead>
            <tr>
                <th></th>
                <th>تصویر محصول</th>
                <th>نام محصول</th>
                <th>قیمت</th>
                <th>تعداد</th>
                <th>قیمت کل</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <img class="removeImage" src="{% static 'IMAGE/logo/removeIcon.png' %}" alt="removeIcon">
                </td>
                <td>
                    <img class="productImage" src="{% static 'IMAGE/product/dress1-1-700x893.jpg' %}" alt="dress1">
                </td>
                <td>لباس مجلسی</td>
                <td>600000 ريال</td>
                <td>
                    <input type="button" value="+">
                    <input type="text" value="1">
                    <input type="button" value="-">
                </td>
                <td>600000 ريال</td>
            </tr>
            <tr>
                <td>
                    <img class="removeImage" src="{% static 'IMAGE/logo/removeIcon.png' %}" alt="removeIcon">
                </td>
                <td>
                    <img class="productImage" src="{% static 'IMAGE/product/hoodie1-1-700x893.jpg' %}" alt="hoodie1">
                </td>
                <td>هودی</td>
                <td>600000 ريال</td>
                <td>
                    <input type="button" value="+">
                    <input type="text" value="2">
                    <input type="button" value="-">
                </td>
                <td>1200000 ريال</td>
            </tr>
            <tr>
                <td>
                    <img class="removeImage" src="{% static 'IMAGE/logo/removeIcon.png' %}" alt="removeIcon">
                </td>
                <td>
                    <img class="productImage" src="{% static 'IMAGE/product/jeans1-1-700x893.jpg' %}" alt="jeans1">
                </td>
                <td>شلوار لی</td>
                <td>400000 ريال</td>
                <td>
                    <input type="button" value="+">
                    <input type="text" value="3">
                    <input type="button" value="-">
                </td>
                <td>1200000 ريال</td>
            </tr>
        </tbody>
    </table>
    <div class="underTable">
        <div class="rightPart">
            <a href="{% url 'checkout' %}"><button>تایید نهایی</button></a>
        </div>
        <div class="leftPart">
            <input type="text" name="giftCode" placeholder="کد تخفیف خود را وارد کنید">
            <a href=""><button>ثبت کد تخفیف</button></a>
        </div>
    </div>
    <div class="factor">
        <table>
            <thead>
                <tr>
                    <th colspan="2">جمع بندی سبد خرید</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>جمع کل سبد خرید</td>
                    <td>3000000 ﷼</td>
                </tr>
                <tr>
                    <td>هزینه ارسال</td>
                    <td>رایگان</td>
                </tr>
                <tr>
                    <td>کد تخفیف</td>
                    <td>ندارد</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th>جمع کل </th>
                    <th>3000000 ﷼</th>
                </tr>
            </tfoot>
        </table>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```
- ### In public Folder, Create checkout.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Checkout.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox checkout">
    <form action="" method="" autocomplete="on">
        <div class="partition">
            <div class="previousAddress">
                <label><input type="checkbox" value="1" name="previousAddress">&nbsp; آردس پیش فرض &nbsp;</label>
                <label><input type="radio" value="1" name="selectedPreviousAddress"> گیلان - رشت - گلسار </label>
                <label><input type="radio" value="1" name="selectedPreviousAddress"> گیلان - رشت - منظریه </label>
                <label><input type="radio" value="1" name="selectedPreviousAddress"> گیلان - رشت - شهریاران </label>
            </div>
            <div class="newAddress">
                <label><input type="checkbox" value="1" name="newAddress">&nbsp; آردس پیش فرض &nbsp;</label>
                <input list="region" name="newAddress" placeholder="کد شهر خود را انتخاب کنید"> 
                <datalist id="region">
                    <option value="1">گیلان - رشت - گلسار</option>
                    <option value="2">گیلان - رشت - رازی </option>
                    <option value="3">گیلان - رشت - گاز</option>
                    <option value="4">گیلان - رشت - معلم</option>
                </datalist>
                <input type="text" name="detail" placeholder="جزئیات آدرس: مثال گلسار - چهار راه اصفهان" maxlength="100">
            </div>
        </div>
        <div class="partition">
            <div class="factor">
                <table>
                    <thead>
                        <tr>
                            <th colspan="2">جمع بندی سبد خرید</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>جمع کل سبد خرید</td>
                            <td>3000000 ﷼</td>
                        </tr>
                        <tr>
                            <td>هزینه ارسال</td>
                            <td>رایگان</td>
                        </tr>
                        <tr>
                            <td>کد تخفیف</td>
                            <td>ندارد</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <th>جمع کل </th>
                            <th>3000000 ﷼</th>
                        </tr>
                    </tfoot>
                </table>
            </div>
            <div class="personalData">
                <table>
                    <thead>
                        <tr>
                            <th colspan="2">مشخصات فردی</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td rowspan="2">مجموعه پل استار</td>
                            <td>013-34911</td>
                        </tr>
                        <tr>
                            <td>info@poulstar.com</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="partition">
            <label>
                <input type="checkbox" value="1" name="acceptTerm">
                &nbsp; <a href="{% url 'tac' %}">قوانین و مقررات</a> سایت را مطالعه کرده و با آگاهی کامل شرایط خرید آنلاین را می پذیرم. &nbsp;
            </label>
            <input type="submit" value="تایید و پرداخت">
        </div>
    </form>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```
- ### In public Folder, Create contact.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Contact.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox contact">
    <h1>تماس با ما</h1>
    <hr>
    <div class="contactBox">
        <form action="" method="" autocomplete="on">
            <input type="text" name="name" placeholder="نام و نام خانوادگی خود را وارد کنید">
            <input type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
            <textarea name="message" placeholder="متن مورد نظر خود را بنویسید"></textarea>
            <input type="submit" value="ارسال کن">
        </form>
    </div>
    <div class="guideBox">
        <p>فرم آزمایشی پروژه پل استار جهت آموزش بهتر و کاردبری تر با ضاهر مناسب جهت ارتباط گیری بیشتر با مبحث تحصیلی می باشد</p>
        <p>شماره تماس: 34911-013</p>
        <p>آدرس: گیلان - رشت - گلسار - چهار راه اصفهان</p>
        <p>پست الکترونیک: info@poulstar.com</p>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```
- ### In public Folder, Create frequencyAndAnswer.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/FrequencyAndAnswer.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox frequencyAndAnswer">
    <h1>پرسش و پاسخ متداول</h1>
    <div class="halfWidth">
        <div class="tabBox">
            <h2>درگاه پرداخت</h2>
            <p>به طور موثر اطلاعات متقابل رسانه ای را بدون ارزش رسانه ای آزاد کنید. به سرعت تحویل به موقع را برای طرحواره های بلادرنگ به حداکثر برسانید. به طور چشمگیری راه حل های کلیک را بدون راه حل های کاربردی حفظ کنید.</p>
            <!-- ****************************** -->
            <div class="headTab">
                <p>چه زمانی پرداخت کنیم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>اگر سفارش شما تا تاریخ تحویل تخمینی نرسیده است، ما اینجا هستیم تا کمک کنیم، اما ارزش بررسی چند چیز را قبل از تماس گرفتن دارد.</p>
                <p>بین 3 تا 5 روز طول می کشد تا سفارش شما از انبار ما ارسال شود، به محض اینکه سفارش شما در راه است، ایمیلی برای تایید ارسال می کنیم. اگر شما انتخاب کرده ایدتحویل استاندارد یا روز بعد برای مشاهده اطلاعات به روز ردیابی، پیوند ردیابی را که در ایمیل ارسال ارسال کرده ایم، بررسی کنید.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>چطوری تخفیف بگیرم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>اکثر تبلیغات به صورت خودکار هنگام تسویه حساب اعمال می شوند.</p>
                <p>اگر کد تخفیف یا کوپن دارید باید در کادری که عبارت «کد کوپن» را دارد وارد کنید، کد تبلیغاتی خود را وارد کنید و روی دکمه اعمال کوپن کلیک کنید.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>چه مقدار بپردازم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>در مواقعی نمی‌توانیم همه اقلامی را که سفارش داده‌اید ارسال کنیم. اگر بخواهید موارد گم شده ای از سفارش خود داشته باشید، ایمیلی برای شما ارسال خواهیم کرد، بنابراین لطفاً صندوق پستی خود را بررسی کنید. برخی از جزئیات نیز ممکن است روی یادداشت اعزام شما چاپ شود.</p>
                <p>ما هر گونه پرداختی را که برای مواردی که ارسال نشده اند بازپرداخت می کنیم. اگر ایمیلی از ما دریافت نکرده‌اید یا اطلاعاتی در مورد یادداشت ارسال شما وجود ندارد، لطفاً از صفحه تماس با ما دیدن کنید و ما مشکل را حل می‌کنیم. برای شما در سریع ترین زمان ممکن</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>آیا میتوانم سفارشم را رهیابی کنم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>سفارش‌های جمع‌آوری شده از فروشگاه به صورت داخلی پیگیری می‌شوند، اما در حال حاضر نمی‌توان آن را به مشتری ارائه کرد. به محض اینکه سفارش شما در فروشگاه ثبت شد، برای شما ایمیل ارسال می کنیم.</p>
                <p>ردیابی ممکن است در برخی از سفارشات بین المللی در دسترس نباشد. لطفاً قبل از تماس، زمان تحویل کامل را در نظر بگیرید.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>آیا باید یک حساب کاربری برای خرید ایجاد کنم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>بله، اما ایجاد یک حساب کاربری واقعاً ساده است و پس از راه‌اندازی می‌توانید سریع‌تر بررسی کنید، آدرس‌های مکرر را ذخیره کنید، سفارش‌های خود را پیگیری کنید و اولین کسی باشید که در مورد مسابقات، پیشنهادات می‌شنوید. و تخفیف.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>سفارشات فروشگاه</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>در صورتی که درخواست ارسال مجموعه از فروشگاه را داشته باشید، پس از تحویل گرفتن سفارش شما به فروشگاه، یک ایمیل و پیامک برای شما ارسال می کنیم و به شما اطلاع می دهیم که سفارش شما آماده تحویل است.</p>
                <p>زمان تحویل از فروشگاهی به فروشگاه دیگر متفاوت است اما معمولاً در عرض 3 تا 5 روز خواهد بود.</p>
            </div>
            <!-- ******************************* -->
        </div>
        <div class="tabBox">
            <h2>خرید</h2>
            <p>بازارهای قدرتمند را از طریق شبکه‌های plug-and-play مدیریت کنید. به طور پویا کاربران B2C را پس از مزایای پایه نصب شده به تعویق بیندازید. به طور چشمگیری همگرایی مشتری محور را تجسم کنید.</p>
            <!-- ****************************** -->
            <div class="headTab">
                <p>سفارش من چیست</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>اگر سفارش شما تا تاریخ تحویل تخمینی نرسیده است، ما اینجا هستیم تا کمک کنیم، اما ارزش بررسی چند چیز را قبل از تماس گرفتن دارد.</p>
                <p>بین 3 تا 5 روز طول می کشد تا سفارش شما از انبار ما ارسال شود، به محض اینکه سفارش شما در راه است، ایمیلی برای تایید ارسال می کنیم. اگر شما انتخاب کرده ایدتحویل استاندارد یا روز بعد برای مشاهده اطلاعات به روز ردیابی، پیوند ردیابی را که در ایمیل ارسال ارسال کرده ایم، بررسی کنید.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>چگونه از کد تبلیغاتی استفاده کنم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>اکثر تبلیغات به صورت خودکار هنگام تسویه حساب اعمال می شوند.</p>
                <p>اگر کد تخفیف یا کوپن دارید باید در کادری که عبارت «کد کوپن» را دارد وارد کنید، کد تبلیغاتی خود را وارد کنید و روی دکمه اعمال کوپن کلیک کنید.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>بخشی از سفارش من گم شده است</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>در مواقعی نمی‌توانیم همه اقلامی را که سفارش داده‌اید ارسال کنیم. اگر بخواهید موارد گم شده ای از سفارش خود داشته باشید، ایمیلی برای شما ارسال خواهیم کرد، بنابراین لطفاً صندوق پستی خود را بررسی کنید. برخی از جزئیات نیز ممکن است روی یادداشت اعزام شما چاپ شود.</p>
                <p>ما هر گونه پرداختی را که برای مواردی که ارسال نشده اند بازپرداخت می کنیم. اگر ایمیلی از ما دریافت نکرده‌اید یا اطلاعاتی در مورد یادداشت ارسال شما وجود ندارد، لطفاً از صفحه تماس با ما دیدن کنید و ما مشکل را حل می‌کنیم. برای شما در سریع ترین زمان ممکن</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>آیا میتوانم سفارشم را رهیابی کنم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>سفارش‌های جمع‌آوری شده از فروشگاه به صورت داخلی پیگیری می‌شوند، اما در حال حاضر نمی‌توان آن را به مشتری ارائه کرد. به محض اینکه سفارش شما در فروشگاه ثبت شد، برای شما ایمیل ارسال می کنیم.</p>
                <p>ردیابی ممکن است در برخی از سفارشات بین المللی در دسترس نباشد. لطفاً قبل از تماس، زمان تحویل کامل را در نظر بگیرید.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>آیا باید یک حساب کاربری برای خرید ایجاد کنم</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>بله، اما ایجاد یک حساب کاربری واقعاً ساده است و پس از راه‌اندازی می‌توانید سریع‌تر بررسی کنید، آدرس‌های مکرر را ذخیره کنید، سفارش‌های خود را پیگیری کنید و اولین کسی باشید که در مورد مسابقات، پیشنهادات می‌شنوید. و تخفیف.</p>
            </div>
            <!-- ******************************* -->
            <!-- ****************************** -->
            <div class="headTab">
                <p>سفارشات فروشگاه</p>
                <span>&#8658;</span>
            </div>
            <div class="bodyTab">
                <p>در صورتی که درخواست ارسال مجموعه از فروشگاه را داشته باشید، پس از تحویل گرفتن سفارش شما به فروشگاه، یک ایمیل و پیامک برای شما ارسال می کنیم و به شما اطلاع می دهیم که سفارش شما آماده تحویل است.</p>
                <p>زمان تحویل از فروشگاهی به فروشگاه دیگر متفاوت است اما معمولاً در عرض 3 تا 5 روز خواهد بود.</p>
            </div>
            <!-- ******************************* -->
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
<script src="{% static 'JS/FAQ.js' %}"></script>
{% endblock %}
```
- ### In public Folder, Create home.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% load tools %}

{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Home.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox">
    <div class="headerImage">
        <div class="rightHeader">
            <img class="imgRightTop" src="{% static 'IMAGE/home/home-header-right-top.jpg' %}" alt="headerRightTop">
            <img class="imgRightBottom" src="{% static 'IMAGE/home/home-header-right-bottom.jpg' %}" alt="headerRightBottom">
        </div>
        <div class="leftHeader">
            <img class="imgleft" src="{% static 'IMAGE/home/home-header-left.jpg' %}" alt="hedareLeft">
        </div>
        
    </div>
    <div class="partition">
        <h1>آخرین محصولات</h1>
        <hr>
    </div>
    <div class="lastProduct">
        {% for product in latestProduct %}
        <div class="imageBox">
            {% if product.discount_id %}
            <span class="discount"></span>
            {% endif %}
            <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="bag1"></a>
            <div class="secondImageBox">
                <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.1.path.url }}" alt="bag1"></a>
                <a href="{% url 'singleProduct' product.id %}"><div>جزئیات</div></a>
            </div>
            <div class="productName">
                <a href="{% url 'singleProduct' product.id %}"><p>{{ product.label }}</p></a>
                <a href="{% url 'singleProduct' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
            </div>
            <div class="tag">
                {% for tag in product.tag_id.all %}
                <span><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></span>,
                {% endfor %}
            </div>
            <div class="price">
                {% if product.discount_id %}
                <del>{{ product.price|showPrice }} ريال</del>
                <ins>{% if product.discount_id.price %}
                    {{ product.price|mines:product.discount_id.price }}
                    {% elif product.discount_id.percent %}
                    {{ product.price|calculateDiscount:product.discount_id.percent }}
                    {% endif %} ريال</ins>
                {% else %}
                <ins>{{ product.price|showPrice }} ريال</ins>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    <div class="partition">
        <h1>آخرین محصولات مردانه</h1>
        <hr>
    </div>
    <div class="menProduct">
        {% for product in latestMenProduct %}
        <div class="imageBox">
            {% if product.discount_id %}
            <span class="discount"></span>
            {% endif %}
            <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="bag1"></a>
            <div class="secondImageBox">
                <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.1.path.url }}" alt="bag1"></a>
                <a href="{% url 'singleProduct' product.id %}"><div>جزئیات</div></a>
            </div>
            <div class="productName">
                <a href="{% url 'singleProduct' product.id %}"><p>{{ product.label }}</p></a>
                <a href="{% url 'singleProduct' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
            </div>
            <div class="tag">
                {% for tag in product.tag_id.all %}
                <span><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></span>,
                {% endfor %}
            </div>
            <div class="price">
                {% if product.discount_id %}
                <del>{{ product.price|showPrice }} ريال</del>
                <ins>{% if product.discount_id.price %}
                    {{ product.price|mines:product.discount_id.price }}
                    {% elif product.discount_id.percent %}
                    {{ product.price|calculateDiscount:product.discount_id.percent }}
                    {% endif %} ريال</ins>
                {% else %}
                <ins>{{ product.price|showPrice }} ريال</ins>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    <div class="partition">
        <h1>آخرین محصولات زنانه</h1>
        <hr>
    </div>
    <div class="womenProduct">
        {% for product in latestWomenProduct %}
        <div class="imageBox">
            {% if product.discount_id %}
            <span class="discount"></span>
            {% endif %}
            <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="bag1"></a>
            <div class="secondImageBox">
                <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.1.path.url }}" alt="bag1"></a>
                <a href="{% url 'singleProduct' product.id %}"><div>جزئیات</div></a>
            </div>
            <div class="productName">
                <a href="{% url 'singleProduct' product.id %}"><p>{{ product.label }}</p></a>
                <a href="{% url 'singleProduct' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
            </div>
            <div class="tag">
                {% for tag in product.tag_id.all %}
                <span><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></span>,
                {% endfor %}
            </div>
            <div class="price">
                {% if product.discount_id %}
                <del>{{ product.price|showPrice }} ريال</del>
                <ins>{% if product.discount_id.price %}
                    {{ product.price|mines:product.discount_id.price }}
                    {% elif product.discount_id.percent %}
                    {{ product.price|calculateDiscount:product.discount_id.percent }}
                    {% endif %} ريال</ins>
                {% else %}
                <ins>{{ product.price|showPrice }} ريال</ins>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```
- ### In public Folder, Create product.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% load tools %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/Product.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox customizeLayout">
    <div class="horizontalPart">
        <div class="horizontalRightPart">
            <ul>
                <li><a href="{% url 'home' %}">خانه</a></li>/
                {% if current_category %}
                    {% if current_category.parent_id %}
                    <li><a href="{% url 'product' current_category.parent_id.id %}">{{ current_category.parent_id }}</a></li>/
                    <li><a href="{% url 'product' current_category.id %}">{{ current_category }}</a></li>
                    {% else %}
                    <li><a href="{% url 'product' current_category.id %}">{{ current_category }}</a></li>
                    {% endif %}
                {% endif %}
                {% if tag %}
                    <li><a href="{% url 'tag' tag.id %}">{{ tag }}</a></li>
                {% endif %}
            </ul>
        </div>
        <div class="horizontalLeftPart">
            <div class="productAmount">
                <p>مجموع محصولات در حال نمایش: </p>
                <span id="counter">17</span>
            </div>
            <div class="sortProduct">
                <select name="sorting" id="sort" oninput="selectMode()">
                    <option value="1">قدیمی ترین</option>
                    <option value="2">جدید ترین</option>
                    <option value="3">ارزان ترین</option>
                    <option value="4">گران ترین</option>
                </select>
            </div>
            <div class="searchProduct">
                <input type="search" name="searchBox" id="searchBox" placeholder="محصول مورد نظر خود را وارد کنید">
                <button id="search" onclick="searchProduct()">&#9935;</button>
            </div>
        </div>
    </div>
    <div class="contectBox">
        <div class="helpPart">
            <div class="latestMenProduct">
                <h1>آخرین محصولات مردانه</h1>
                {% for product in latestMenProduct  %}
                <div class="smallShowProduct">
                    <div class="smallImage">
                        <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="hoodie1"></a>
                    </div>
                    <div class="smallDetail">
                        <a href="{% url 'singleProduct' product.id %}"><p>{{ product }}</p></a>
                        {% if product.discount_id %}
                        <del>{{ product.price|showPrice }} ريال</del>
                        <ins>{% if product.discount_id.price %}
                            {{ product.price|mines:product.discount_id.price }}
                            {% elif product.discount_id.percent %}
                            {{ product.price|calculateDiscount:product.discount_id.percent }}
                            {% endif %} ريال</ins>
                        {% else %}
                        <ins>{{ product.price|showPrice }} ريال</ins>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
            <hr>
            <div class="latestWomenProduct">
                <h1>آخرین محصولات زنانه</h1>
                {% for product in latestWomenProduct  %}
                <div class="smallShowProduct">
                    <div class="smallImage">
                        <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="hoodie1"></a>
                    </div>
                    <div class="smallDetail">
                        <a href="{% url 'singleProduct' product.id %}"><p>{{ product }}</p></a>
                        {% if product.discount_id %}
                        <del>{{ product.price|showPrice }} ريال</del>
                        <ins>{% if product.discount_id.price %}
                            {{ product.price|mines:product.discount_id.price }}
                            {% elif product.discount_id.percent %}
                            {{ product.price|calculateDiscount:product.discount_id.percent }}
                            {% endif %} ريال</ins>
                        {% else %}
                        <ins>{{ product.price|showPrice }} ريال</ins>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
            <hr>
            <div class="allTags">
                <h1>تگ ها</h1>
                {% for tag in tags %}
                <button><a href="{% url 'tag' tag.id %}">{{ tag }}</a></button>
                {% endfor %}
            </div>
        </div>
        <div id="productBox" class="showProduct">
            {% for product in products %}
            <div id="{{ product.id }}" data-price="{% if product.discount_id %}
            {% if product.discount_id.price %}
                {{ product.price|mines:product.discount_id.price }}
                {% elif product.discount_id.percent %}
                {{ product.price|calculateDiscount:product.discount_id.percent }}
                {% endif %}
            {% else %}
            {{ product.price|showPrice }}
            {% endif %}" data-name="{{ product }}" class="imageBox">
                {% if product.discount_id %}
                <span class="discount"></span>
                {% endif %}
                <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="bag1"></a>
                <div class="secondImageBox">
                    <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.1.path.url }}" alt="bag1"></a>
                    <a href="{% url 'singleProduct' product.id %}"><div>جزئیات</div></a>
                </div>
                <div class="productName">
                    <a href="{% url 'singleProduct' product.id %}"><p>{{ product.label }}</p></a>
                    <a href="{% url 'singleProduct' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
                </div>
                <div class="tag">
                    {% for tag in product.tag_id.all %}
                    <span><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></span>,
                    {% endfor %}
                </div>
                <div class="price">
                    {% if product.discount_id %}
                    <del>{{ product.price|showPrice }} ريال</del>
                    <ins>{% if product.discount_id.price %}
                        {{ product.price|mines:product.discount_id.price }}
                        {% elif product.discount_id.percent %}
                        {{ product.price|calculateDiscount:product.discount_id.percent }}
                        {% endif %} ريال</ins>
                    {% else %}
                    <ins>{{ product.price|showPrice }} ريال</ins>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <div class="horizontalPart">
        <div id="pagination" class="pagination"></div>
    </div>
</div>
{% endblock %}

{% block js %}
<script src="{% static 'JS/Product.js' %}"></script>
{% endblock %}
```
- ### In public Folder, Create singleProduct.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% load tools %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/SingleProduct.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox singleProduct">
    <div class="verticalPart">
        <div class="productRoute">
            <ul>
                <li><a href="{% url 'home' %}">خانه</a></li>/
                {% if product.category_id %}
                    {% if product.category_id.parent_id %}
                    <li><a href="{% url 'product' product.category_id.parent_id.id %}">{{ product.category_id.parent_id }}</a></li>/
                    <li><a href="{% url 'product' product.category_id.id %}">{{ product.category_id }}</a></li>
                    {% else %}
                    <li><a href="{% url 'product' product.category_id.id %}">{{ product.category_id }}</a></li>
                    {% endif %}
                {% endif %}
            </ul>
        </div>
        <div class="productDescription">
            <h1>{{ product.label }}</h1>
            <h2>{{ product.description }}</h2>
            {% if product.discount_id %}
            <del>{{ product.price|showPrice }} ريال</del>
            <ins>{% if product.discount_id.price %}
                {{ product.price|mines:product.discount_id.price }}
                {% elif product.discount_id.percent %}
                {{ product.price|calculateDiscount:product.discount_id.percent }}
                {% endif %} ريال</ins>
            {% else %}
            <ins>{{ product.price|showPrice }} ريال</ins>
            {% endif %}
        </div>
        <div class="productCounter">
            <form action="">
                <input type="button" value="+" onclick="increment()">
                <input type="number" name="quantity" value="1" id="productQuantity">
                <input type="button" value="-" onclick="decrement()">
                <input type="submit" value="افزودن به سبد خرید">
            </form>
        </div>
        <div class="productDetail">
            <div class="productCategory">
                <span>دسته بندی: </span>
                <p><a href="{% url 'product' product.category_id.id %}">{{ product.category_id }}</a></p>
            </div>
            <div class="productTag">
                <span>تگ ها: </span>
                {% for tag in product.tag_id.all %}
                <p><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></p>، 
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="verticalPart">
        <div class="productImage">
            <img id="show" src="{{ product.productImages.all.0.path.url }}" alt="dress1">
        </div>
        <div class="allImage">
            <img onclick="selectFirstImage()" id="first" src="{{ product.productImages.all.0.path.url }}" alt="dress1">
            <img onclick="selectSecondImage()" id="second" src="{{ product.productImages.all.1.path.url }}" alt="dress1">
        </div>
    </div>
    <div class="horizontalPart">
        <div class="tab">
            <button onclick="descriptionTab()">توضیحات</button>
            <button onclick="commentTab()">نظر ها (0)</button>
        </div>
        <div id="description" class="tabcontent">
            <p>{{ product.label }}</p>
            <p>{{ product.description }}</p>
        </div>
        <div id="comment" class="tabcontent">
            {% for comment in comments %}
            <div class="user">
                <p>{{ comment.user_id }}</p>
            </div>
            <div class="userComment">
                <p>{{ comment.description }}</p>
            </div>
            {% endfor %}
            <hr>
            {% if user.is_authenticated %}
            <div class="newComment">
                <form action="">
                    <textarea name="comment" placeholder="نظر خود را بنویسید ..."></textarea>
                    <input type="submit" value="ثبت نظر">
                </form>
            </div>
            {% endif %}
        </div>
    </div>
    <div class="partition">
        <h1>آخرین محصولات</h1>
        <hr>
    </div>
    <div class="relatedProduct">
        {% for product in latestProduct %}
        <div class="imageBox">
            {% if product.discount_id %}
            <span class="discount"></span>
            {% endif %}
            <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.0.path.url }}" alt="bag1"></a>
            <div class="secondImageBox">
                <a href="{% url 'singleProduct' product.id %}"><img src="{{ product.productImages.all.1.path.url }}" alt="bag1"></a>
                <a href="{% url 'singleProduct' product.id %}"><div>جزئیات</div></a>
            </div>
            <div class="productName">
                <a href="{% url 'singleProduct' product.id %}"><p>{{ product.label }}</p></a>
                <a href="{% url 'singleProduct' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
            </div>
            <div class="tag">
                {% for tag in product.tag_id.all %}
                <span><a href="{% url 'tag' tag.id %}">{{ tag.label }}</a></span>,
                {% endfor %}
            </div>
            <div class="price">
                {% if product.discount_id %}
                <del>{{ product.price|showPrice }} ريال</del>
                <ins>{% if product.discount_id.price %}
                    {{ product.price|mines:product.discount_id.price }}
                    {% elif product.discount_id.percent %}
                    {{ product.price|calculateDiscount:product.discount_id.percent }}
                    {% endif %} ريال</ins>
                {% else %}
                <ins>{{ product.price|showPrice }} ريال</ins>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}

{% block js %}
<script src="{% static 'JS/SingleProduct.js' %}"></script>
{% endblock %}
```
- ### In public Folder, Create termAndCondition.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
<link rel="stylesheet" href="{% static 'CSS/TermAndCondition.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox termAndCondition">
    <h1>قوانین و مقررات</h1>
    <h2>عمومی</h2>
    <hr>
    <div>
        <p>
            دسترسی و استفاده از این وب سایت و محصولات و خدمات قابل ارائه از طریق این وب سایت مشمول شرایط، شرایط و تذکرات زیر است. 
            با استفاده از خدمات، شما با تمام شرایط خدمات موافقت می کنید، همانطور که ممکن است هر از گاهی توسط ما به روز شود.
            شما باید این صفحه را مرتباً بررسی کنید تا از تغییراتی که ممکن است در شرایط خدمات ایجاد کرده باشیم مطلع شوید.
        </p>
        <p>
            دسترسی به این وب سایت به صورت موقت مجاز است و ما این حق را برای خود محفوظ می داریم که خدمات را بدون اطلاع قبلی لغو یا اصلاح کنیم. 
            اگر به هر دلیلی این وب سایت در هر زمان و یا برای هر دوره ای در دسترس نباشد، ما مسئولیتی نخواهیم داشت.
            گاهی اوقات، ممکن است دسترسی به برخی از بخش ها یا تمام این وب سایت را محدود کنیم.
        </p>
        <p>
            این وب سایت همچنین حاوی پیوندهایی به وب سایت های دیگر است که توسط پل استار اداره نمی شوند.
            لامبدا هیچ کنترلی بر سایت های لینک شده ندارد و هیچ مسئولیتی در قبال آن ها یا هر گونه ضرر یا آسیبی که ممکن است در اثر استفاده شما از آنها ایجاد شود، نمی پذیرد.
            استفاده شما از سایت های لینک شده تابع شرایط استفاده و خدمات مندرج در هر یک از این سایت ها خواهد بود.
        </p>
    </div>
    <h2>حریم خصوصی</h2>
    <hr>
    <div>
        <p>
            دسترسی و استفاده از این وب سایت و محصولات و خدمات قابل ارائه از طریق این وب سایت مشمول شرایط، شرایط و تذکرات زیر است. 
            با استفاده از خدمات، شما با تمام شرایط خدمات موافقت می کنید، همانطور که ممکن است هر از گاهی توسط ما به روز شود.
            شما باید این صفحه را مرتباً بررسی کنید تا از تغییراتی که ممکن است در شرایط خدمات ایجاد کرده باشیم مطلع شوید.
        </p>
        <p>
            دسترسی به این وب سایت به صورت موقت مجاز است و ما این حق را برای خود محفوظ می داریم که خدمات را بدون اطلاع قبلی لغو یا اصلاح کنیم. 
            اگر به هر دلیلی این وب سایت در هر زمان و یا برای هر دوره ای در دسترس نباشد، ما مسئولیتی نخواهیم داشت.
            گاهی اوقات، ممکن است دسترسی به برخی از بخش ها یا تمام این وب سایت را محدود کنیم.
        </p>
        <p>
            این وب سایت همچنین حاوی پیوندهایی به وب سایت های دیگر است که توسط پل استار اداره نمی شوند.
            لامبدا هیچ کنترلی بر سایت های لینک شده ندارد و هیچ مسئولیتی در قبال آن ها یا هر گونه ضرر یا آسیبی که ممکن است در اثر استفاده شما از آنها ایجاد شود، نمی پذیرد.
            استفاده شما از سایت های لینک شده تابع شرایط استفاده و خدمات مندرج در هر یک از این سایت ها خواهد بود.
        </p>
    </div>
    <h2>ثبت نام</h2>
    <hr>
    <div>
        <p>
            دسترسی و استفاده از این وب سایت و محصولات و خدمات قابل ارائه از طریق این وب سایت مشمول شرایط، شرایط و تذکرات زیر است. 
            با استفاده از خدمات، شما با تمام شرایط خدمات موافقت می کنید، همانطور که ممکن است هر از گاهی توسط ما به روز شود.
            شما باید این صفحه را مرتباً بررسی کنید تا از تغییراتی که ممکن است در شرایط خدمات ایجاد کرده باشیم مطلع شوید.
        </p>
        <p>
            دسترسی به این وب سایت به صورت موقت مجاز است و ما این حق را برای خود محفوظ می داریم که خدمات را بدون اطلاع قبلی لغو یا اصلاح کنیم. 
            اگر به هر دلیلی این وب سایت در هر زمان و یا برای هر دوره ای در دسترس نباشد، ما مسئولیتی نخواهیم داشت.
            گاهی اوقات، ممکن است دسترسی به برخی از بخش ها یا تمام این وب سایت را محدود کنیم.
        </p>
        <p>
            این وب سایت همچنین حاوی پیوندهایی به وب سایت های دیگر است که توسط پل استار اداره نمی شوند.
            لامبدا هیچ کنترلی بر سایت های لینک شده ندارد و هیچ مسئولیتی در قبال آن ها یا هر گونه ضرر یا آسیبی که ممکن است در اثر استفاده شما از آنها ایجاد شود، نمی پذیرد.
            استفاده شما از سایت های لینک شده تابع شرایط استفاده و خدمات مندرج در هر یک از این سایت ها خواهد بود.
        </p>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}
```
- ### Update models.py File
```bash
from django.db import models
from django.contrib.auth import get_user_model

class Contacts (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=14)
    description = models.CharField(max_length=10000)
    status = models.BooleanField()

    def __str__(self):
        return self.description

class Discounts (models.Model):
    label = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    gift_code = models.CharField(max_length=256, blank=True)
    status = models.BooleanField()

    def __str__(self):
        return self.label
        
class Tags (models.Model):
    label = models.CharField(max_length=256)
    status = models.BooleanField()

    def __str__(self):
        return self.label   
     
class Categories (models.Model):
    parent_id = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    label = models.CharField(max_length=256)
    status = models.BooleanField()

    def __str__(self):
        return self.label
    
class Regions (models.Model):
    label = models.CharField(max_length=256)
    status = models.BooleanField()

    def __str__(self):
        return self.label

class Cities (models.Model):
    region_id = models.ForeignKey(to=Regions, on_delete=models.CASCADE)
    label = models.CharField(max_length=256)
    status = models.BooleanField()

    def __str__(selft):
        return selft.label 

class Addresses (models.Model):
    city_id = models.ForeignKey(to=Cities, on_delete=models.CASCADE)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    detail = models.CharField(max_length=1000)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.detail


class Products (models.Model):
    tag_id = models.ManyToManyField(to=Tags, related_name='product_id')
    discount_id = models.ForeignKey(to=Discounts, on_delete=models.CASCADE, null=True, blank=True)
    category_id = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    label = models.CharField(max_length=256)
    description = models.CharField(max_length=10000)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField()

    def __str__(self):
        return self.label

class ProductImages (models.Model):
    product_id = models.ForeignKey(to=Products, on_delete=models.CASCADE, related_name='productImages')
    path = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_id.label
    
class Comments (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    status = models.BooleanField()

    def __str__(self):
        return self.description

class Orders (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address_id = models.ForeignKey(to=Addresses, on_delete=models.CASCADE)
    discount_id = models.ForeignKey(to=Discounts, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    pay_price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField()

    def __str__(self):
        return self.user_id.username

class OrderListItems (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField()

    def __str__(self):
        return self.user_id.username
```
- ### Update admin.py File
```bash
from django.contrib import admin
from . import models

admin.site.register(models.Categories)
admin.site.register(models.Tags)
admin.site.register(models.Discounts)
admin.site.register(models.Regions)
admin.site.register(models.Cities)
admin.site.register(models.Addresses)
admin.site.register(models.Comments)

class ProductImagesAdmin(admin.StackedInline):
    model = models.ProductImages

class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    class Meta:
        model = models.Products

admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.ProductImages)
admin.site.register(models.Orders)
admin.site.register(models.OrderListItems)
admin.site.register(models.Contacts)
```
- ### Update views.py File
```bash
from django.shortcuts import render, get_object_or_404
from django.urls import resolve
from . import models

def cart(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/cart.html', context)

def checkout(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/checkout.html', context)

def contact(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/contact.html', context)

def frequency_and_answer(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/frequencyAndAnswer.html', context)

def home(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    
    allCategories = models.Categories.objects.all()
    mainCategories = models.Categories.objects.filter(parent_id = None)
    
    latestProduct = models.Products.objects.order_by('-id')[:4]
    
    menCategory = []
    for category in allCategories:
        if category.id == 1 or (category.parent_id != None and category.parent_id.id == 1):
            menCategory.append(category.id)
    latestMenProduct = models.Products.objects.filter(category_id__in=menCategory).order_by('-id')[:6]
    
    WomenCategory = []
    for category in allCategories:
        if category.id == 2 or (category.parent_id != None and category.parent_id.id == 2):
            WomenCategory.append(category.id)
    latestWomenProduct = models.Products.objects.filter(category_id__in=WomenCategory).order_by('-id')[:6]
    
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : mainCategories,
        'latestProduct' : latestProduct,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
    }
    return render(request, 'public/home.html', context)    

def product(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    current_category = get_object_or_404(models.Categories, pk = pk)
    tags = models.Tags.objects.all()
    allCategories = models.Categories.objects.all()
    menCategory = []
    for category in allCategories:
        if category.id == 1 or (category.parent_id != None and category.parent_id.id == 1):
            menCategory.append(category.id)
    latestMenProduct = models.Products.objects.filter(category_id__in=menCategory).order_by('-id')[:3]
    WomenCategory = []
    for category in allCategories:
        if category.id == 2 or (category.parent_id != None and category.parent_id.id == 2):
            WomenCategory.append(category.id)
    latestWomenProduct = models.Products.objects.filter(category_id__in=WomenCategory).order_by('-id')[:3]
    category_IDs = []
    for category in allCategories:
        if category.id == pk or (category.parent_id != None and category.parent_id.id == pk):
            category_IDs.append(category.id)
    products = models.Products.objects.filter(category_id__in=category_IDs).order_by('-id')
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'current_category' : current_category,
        'tag' : False,
        'tags' : tags,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
        'products' : products,
    }
    return render(request, 'public/product.html', context)

def tag(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    current_tag = get_object_or_404(models.Tags, pk = pk)
    tags = models.Tags.objects.all()
    allCategories = models.Categories.objects.all()
    menCategory = []
    for category in allCategories:
        if category.id == 1 or (category.parent_id != None and category.parent_id.id == 1):
            menCategory.append(category.id)
    latestMenProduct = models.Products.objects.filter(category_id__in=menCategory).order_by('-id')[:3]
    WomenCategory = []
    for category in allCategories:
        if category.id == 2 or (category.parent_id != None and category.parent_id.id == 2):
            WomenCategory.append(category.id)
    latestWomenProduct = models.Products.objects.filter(category_id__in=WomenCategory).order_by('-id')[:3]
    products = models.Products.objects.filter(tag_id=pk).order_by('-id')
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'current_category' : False,
        'tag' : current_tag,
        'tags' : tags,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
        'products' : products,
    }
    return render(request, 'public/product.html', context)

def single_product(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    product = get_object_or_404(models.Products, pk = pk)
    comments = models.Comments.objects.filter(product_id=pk)
    latestProduct = models.Products.objects.order_by('-id')[:3]
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'product' : product,
        'comments' : comments,
        'latestProduct' : latestProduct,
    }
    return render(request, 'public/singleProduct.html', context)

def term_and_condition(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/termAndCondition.html', context)

def dashboard(request):
    return render(request, 'dashboard/dashboard.html') 
```
- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('frequency-and-answer/', views.frequency_and_answer, name='faq'),
    path('<int:pk>/product/', views.product, name='product'),
    path('<int:pk>/tag/', views.tag, name='tag'),
    path('<int:pk>/single-product/', views.single_product, name='singleProduct'),
    path('term-and-condition/', views.term_and_condition, name='tac'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```
## Install Pillow
- ### Install Command
```bash
pip install pillow
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
