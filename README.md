# Complete Session Part In Shop Project

## Create app session
### In Windows
```bash
py manage.py startapp session
```
### In MacOS
```bash
python manage.py startapp session
```
### In Linux
```bash
python3 manage.py startapp session
```

## In Session App
- ### Update views.py File
```bash
from django.shortcuts import redirect
from shop.models import Discounts

def add_to_session(request, pk):
    flag_for_Loop = True
    quantity = 1
    if request.method == 'POST':
        if request.POST['quantity']:
            quantity = int(request.POST['quantity'])
    if 'cart' in request.session:
        if len(request.session['cart']) > 0:
            for item in request.session['cart']:
                if item[0] == pk: 
                    request.session['cart'][request.session['cart'].index(item)][1] += quantity
                    flag_for_Loop = False
                    break
            if flag_for_Loop:
                request.session['cart'].append([pk, quantity])
        else:
            request.session['cart'].append([pk, quantity])
    else:
        request.session['cart'] = [[pk, quantity]]

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))

def mines_from_session(request, pk):
    if 'cart' in request.session:
        for item in request.session['cart']:
            if item[0] == pk:
                if request.session['cart'][request.session['cart'].index(item)][1] > 1:
                    request.session['cart'][request.session['cart'].index(item)][1] -= 1
                else:
                    del request.session['cart'][request.session['cart'].index(item)]

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))

def plus_from_session(request, pk):
    if 'cart' in request.session:
        for item in request.session['cart']:
            if item[0] == pk:
                request.session['cart'][request.session['cart'].index(item)][1] += 1  

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))
  
def delete_item_from_session(request, pk):
    if 'cart' in request.session:
        for item in request.session['cart']:
            if item[0] == pk:
                del request.session['cart'][request.session['cart'].index(item)]

    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))

def add_discount(request):
    if request.method == 'POST':
        if request.POST['giftCode']:
            gift_code = request.POST['giftCode']
            discount = Discounts.objects.filter(gift_code=gift_code).first()
            if discount:
                if discount.price:
                    if 'discount' in request.session:
                        if len(request.session['discount']) > 0:
                            request.session['discount'].append([int(discount.price)])
                        else:
                            request.session['discount'] = [[int(discount.price)]]
                    else:
                        request.session['discount'] = [[int(discount.price)]]
                    
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))
```
- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('add-to-session/<int:pk>/', views.add_to_session, name='add_to_session'),
    path('mines-from-session/<int:pk>/', views.mines_from_session, name='mines_from_session'),
    path('plus-from-session/<int:pk>/', views.plus_from_session, name='plus_from_session'),
    path('delete-item-from-session/<int:pk>/', views.delete_item_from_session, name='delete_item_from_session'),
    path('add-discount/', views.add_discount, name='add_discount'),
]
```

## In Lib Folder
- ### Create session.py File
```bash
from shop import models

def get_cart_session(request):
    cart = request.session.get('cart', None)
    ids_list = []
    if not cart == None:
        for item in cart:
            ids_list.append(item[0])
    selected_product_in_cart = models.Products.objects.filter(id__in=ids_list)
    final_cart_lists = []
    total_price = 0
    for selected_item in selected_product_in_cart:
        for item in cart:
            if selected_item.id == item[0]:
                final_cart_lists.append({'cart_product':selected_item, 'quantity':item[1]})
                if selected_item.discount_id:
                    if selected_item.discount_id.price:
                        price = selected_item.price - selected_item.discount_id.price
                        total_price += price * item[1]
                    elif selected_item.discount_id.percent:
                        computed_price = selected_item.price * selected_item.discount_id.percent/100
                        price = selected_item.price - computed_price
                        total_price += price * item[1]
                else:
                    total_price += selected_item.price * item[1]
                    
    return  final_cart_lists, total_price

def get_discount_session(request):
    total_discount = 0
    discount = request.session.get('discount', None)
    if discount:
        for item in discount:
            total_discount += item[0]
    return total_discount

def clear_session(request, session_name):
    request.session[session_name].clear()
    request.session.modified = True
```
- ### Update __init__.py File
```bash
from lib.error_handling import *
from lib.session import *
```

## In Config Folder
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
    'session',
]
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
    path('session/', include('session.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## In Accounts app
- ### Update views.py File
```bash
from lib import error_progres, get_cart_session
```
```bash
def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            password = request.POST['password']
            user = CustomUser.objects.filter(phone=phone).first()
            if user:
                login_user = authenticate(username=user.username, password=password)
                if login_user is not None:
                    loginRequest(request, login_user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'رمز عبور صحیح نیست')   
            else:
                messages.error(request, 'کاربری با این شماره تماس وجود ندارد')    
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)

    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'registration/login.html', context)
```
```bash
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            username = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            password = request.POST['password']
            username_state = False
            phone_state = False
            email_state = False
            if CustomUser.objects.filter(username=username).first():
                messages.error(request, 'نام کاربری مورد نظر قبلا ثبت شده است')
                username_state = True
            if CustomUser.objects.filter(phone=phone).first():
                messages.error(request, 'شماره تماس مورد نظر قبلا ثبت شده است')
                phone_state = True
            if CustomUser.objects.filter(email=email).first():
                messages.error(request, 'پست الکترونیک مورد نظر قبلا ثبت شده است')
                email_state = True
            if (username_state == False and phone_state == False and email_state == False):
                new_user = CustomUser.objects.create(
                    username = username,
                    phone = phone,
                    email = email,
                )
                new_user.set_password(password)
                new_user.save()
                loginRequest(request, new_user)
                return redirect('dashboard')    
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'registration/signup.html', context)
```
## In Root Templates Folder
- ### Update publicLayout.html File
```bash
{% load static %}
{% load tools %}
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
                <span class="ShopingCartCounter center dropbtn">{{ final_cart_lists|length }}</span>
                <div class="dropdown-content">
                    <a class="btn" href="{% url 'cart' %}">فاکتور کن</a>
                    {% for product in final_cart_lists %}
                    <a class="linkMenu" href="{% url 'singleProduct' product.cart_product.id %}">
                        <img class="cart" src="{{ product.cart_product.productImages.all.0.path.url }}" alt="dress1-1">
                        <div class="box">
                            <div class="detail">
                                <span>{{ product.cart_product.label }}</span>
                                {% if product.cart_product.discount_id %}
                                <ins>{% if product.cart_product.discount_id.price %}
                                    {{ product.cart_product.price|mines:product.cart_product.discount_id.price|multiple:product.quantity }}
                                    {% elif product.cart_product.discount_id.percent %}
                                    {{ product.cart_product.price|calculateDiscount:product.cart_product.discount_id.percent|multiple:product.quantity }}
                                    {% endif %} ريال</ins>
                                {% else %}
                                <ins>{{ product.cart_product.price|multiple:product.quantity }} ريال</ins>
                                {% endif %}
                            </div>
                        </div>
                    </a>
                    {% endfor %}
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
## In Shop App
- ### Update Tools.py File in templatetags Folder
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
@register.filter()
def multiple(value, arg):
    final_price = value * arg
    return int(final_price)
```
- ### In templates Folder, In public Folder, Update cart.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% load tools %}
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
            {% for product in final_cart_lists %}
            <tr>
                <td>
                    <a href="{% url 'delete_item_from_session' product.cart_product.id %}"><img class="removeImage" src="{% static 'IMAGE/logo/removeIcon.png' %}" alt="removeIcon"></a>
                </td>
                <td>
                    <img class="productImage" src="{{ product.cart_product.productImages.all.0.path.url }}" alt="dress1">
                </td>
                <td>{{ product.cart_product.label }}</td>
                <td>{% if product.cart_product.discount_id %}
                    {% if product.cart_product.discount_id.price %}
                        {{ product.cart_product.price|mines:product.cart_product.discount_id.price }}
                        {% elif product.cart_product.discount_id.percent %}
                        {{ product.cart_product.price|calculateDiscount:product.cart_product.discount_id.percent }}
                        {% endif %}
                    {% else %}
                    {{ product.cart_product.price }}
                    {% endif %} ريال</td>
                <td>
                    <a href="{% url 'plus_from_session'  product.cart_product.id %}"><input type="button" value="+"></a>
                    <input type="text" value="{{ product.quantity }}">
                    <a href="{% url 'mines_from_session'  product.cart_product.id %}"><input type="button" value="-"></a>
                </td>
                <td>
                    {% if product.cart_product.discount_id %}
                    {% if product.cart_product.discount_id.price %}
                        {{ product.cart_product.price|mines:product.cart_product.discount_id.price|multiple:product.quantity }}
                        {% elif product.cart_product.discount_id.percent %}
                        {{ product.cart_product.price|calculateDiscount:product.cart_product.discount_id.percent|multiple:product.quantity }}
                        {% endif %}
                    {% else %}
                    {{ product.cart_product.price|multiple:product.quantity }}
                    {% endif %} ريال
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="underTable">
        <div class="rightPart">
            <a href="{% url 'checkout' %}"><button>تایید نهایی</button></a>
        </div>
        <div class="leftPart">
            <form method="POST" action="{% url 'add_discount' %}">
                {% csrf_token %}
                <input type="text" name="giftCode" placeholder="کد تخفیف خود را وارد کنید">
                <a href=""><button>ثبت کد تخفیف</button></a>
            </form>
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
                    <td>
                        
                        {% if total_price > 1 %}
                        {{ total_price }}ريال
                        {% else %}
                        سبد خرید خالی است
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <td>هزینه ارسال</td>
                    <td>رایگان</td>
                </tr>
                <tr>
                    <td>کد تخفیف</td>
                    <td>
                        {% if total_discount %}
                        {{ total_discount }}ريال
                        {% else %}
                        ندارد   
                        {% endif %}
                    </td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th>جمع کل </th>
                    <th>{{ total_price|mines:total_discount }} ﷼</th>
                </tr>
            </tfoot>
        </table>
    </div>
</div>
{% endblock %}

{% block js %}

{% endblock %}


```
- ### In templates Folder, In public Folder, Update checkout.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
{% load tools %}
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
                            <td>
                                {% if total_price > 1 %}
                                {{ total_price }}ريال
                                {% else %}
                                سبد خرید خالی است
                                {% endif %}
                            </td>
                        </tr>
                        <tr>
                            <td>هزینه ارسال</td>
                            <td>رایگان</td>
                        </tr>
                        <tr>
                            <td>کد تخفیف</td>
                            <td>
                                {% if total_discount %}
                                {{ total_discount }}ريال
                                {% else %}
                                ندارد   
                                {% endif %}
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <th>جمع کل </th>
                            <th>{{ total_price|mines:total_discount }} ﷼</th>
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
- ### In templates Folder, In public Folder, Update home.html File
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
                <a href="{% url 'add_to_session' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
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
                <a href="{% url 'add_to_session' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
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
                <a href="{% url 'add_to_session' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
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
- ### In templates Folder, In public Folder, Update product.html File
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
                    <a href="{% url 'add_to_session' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
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
- ### In templates Folder, In public Folder, Update singleProduct.html File
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
            <form method="POST" action="{% url 'add_to_session' product.id %}">
                {% csrf_token %}
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
                <a href="{% url 'add_to_session' product.id %}"><img src="{% static 'IMAGE/menu/ShopingCartLogo.png' %}" alt="ShopingCartLogo"></a>
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
- ### Update views.py File
```bash
from lib import error_progres, get_cart_session, get_discount_session
```
```bash
def cart(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    total_discount = get_discount_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
        'total_price' : total_price,
        'total_discount' : total_discount,
    }
    return render(request, 'public/cart.html', context)
```
```bash
@login_required
def checkout(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    total_discount = get_discount_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
        'total_price' : total_price,
        'total_discount' : total_discount,
    }
    return render(request, 'public/checkout.html', context)
```
```bash
def contact(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/contact.html', context)
```
```bash
def frequency_and_answer(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/frequencyAndAnswer.html', context)
```
```bash
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
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : mainCategories,
        'latestProduct' : latestProduct,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/home.html', context)
```
```bash
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
    final_cart_lists, total_price = get_cart_session(request)
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
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/product.html', context)
```
```bash
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
    final_cart_lists, total_price = get_cart_session(request)
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
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/product.html', context)
```
```bash
def single_product(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    product = get_object_or_404(models.Products, pk = pk)
    comments = models.Comments.objects.filter(product_id=pk)
    latestProduct = models.Products.objects.order_by('-id')[:3]
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'product' : product,
        'comments' : comments,
        'latestProduct' : latestProduct,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/singleProduct.html', context)
```
```bash
def term_and_condition(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    final_cart_lists, total_price = get_cart_session(request)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
    }
    return render(request, 'public/termAndCondition.html', context)
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
