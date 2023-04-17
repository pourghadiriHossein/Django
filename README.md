# Start Shop Project

## shop app
- ### Create forms.py File
```bash
from django import forms

class Update_Profile(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=100,
    error_messages={
        'required' : 'نام کاربری خود را وارد کنید',
        'min_length' : 'نام کاربری شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'نام کاربری شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })
    phone = forms.CharField(required=True, min_length=11, max_length=14,
    error_messages={
        'required' : 'شماره تماس خود را وارد کنید',
        'min_length' : 'شماره تماس شما نمی تواند کمتر از 11 کاراکتر باشد',
        'max_length' : 'شماره تماس شما نمی تواند بیشتر از 14 کاراکتر باشد',
    })
    email = forms.CharField(required=True, min_length=10, max_length=100,
    error_messages={
        'required' : 'پست الکترونیک خود را وارد کنید',
        'min_length' : 'پست الکترونیک شما نمی تواند کمتر از 10 کاراکتر باشد',
        'max_length' : 'پست الکترونیک شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })

class Update_Address(forms.Form):
    city_id = forms.IntegerField(required=True, min_value=1,
    error_messages={
        'required' : 'استان مورد نظر خود را وارد کنید',
        'min_value' : 'مشکل فنی؛ با پشتیبانی تماس بگیرید',
    })
    detail = forms.CharField(required=True, min_length=4, max_length=1000,
    error_messages={
        'required' : 'جزئیات آدرس خود را وارد کنید',
        'min_length' : 'جزئیات آدرس شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'جزئیات آدرس شما نمی تواند بیشتر از 1000 کاراکتر باشد',
    })
```
- ### Update views.py File
```bash
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve
from . import models
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from django.contrib import messages
from .forms import Update_Profile, Update_Address
from lib import error_progres

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

@login_required
def dashboard(request):
    user_addresses = models.Addresses.objects.filter(user_id=request.user.id)
    regions = models.Regions.objects.all()
    cities = models.Cities.objects.all()
    user_comments = models.Comments.objects.filter(user_id=request.user.id)
    user_orders = models.Orders.objects.filter(user_id=request.user.id)
    context = {
        'addresses' : user_addresses,
        'regions' : regions,
        'cities' : cities,
        'comments' : user_comments,
        'orders' : user_orders,
    }
    return render(request, 'dashboard/dashboard.html',context)

@login_required
def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = Update_Profile(request.POST)
        if form.is_valid():
            username = request.POST['username']
            phone = request.POST['phone']
            email = request.POST['email']
            username_state = False
            phone_state = False
            email_state = False
            if not request.user.username == username:
                if CustomUser.objects.filter(username=username).first():
                    messages.error(request, 'نام کاربری مورد نظر قبلا ثبت شده است')
                    username_state = True
            if not request.user.phone == phone:
                if CustomUser.objects.filter(phone=phone).first():
                    messages.error(request, 'شماره تماس مورد نظر قبلا ثبت شده است')
                    phone_state = True
            if not request.user.email == email:    
                if CustomUser.objects.filter(email=email).first():
                    messages.error(request, 'پست الکترونیک مورد نظر قبلا ثبت شده است')
                    email_state = True

            if (username_state == False and phone_state == False and email_state == False):
                CustomUser.objects.update(
                    username = username,
                    phone = phone,
                    email = email,
                )
                messages.success(request, 'ویرایش شما با موفقیت انجام شد')
                return redirect('dashboard')  
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)        
    return redirect('dashboard')   
 
@login_required
def update_address(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        address = get_object_or_404(models.Addresses, pk=pk)
        if not address:
            messages.error(request, 'دسترسی غیرمجاز')
            return redirect('logout')
        else:
            if not address.user_id.id == request.user.id:
                messages.error(request, 'دسترسی غیرمجاز')
                return redirect('logout')
        form = Update_Address(request.POST)
        if form.is_valid():
            city_id = request.POST['city_id']
            detail = request.POST['detail']
            city = models.Cities.objects.filter(id=city_id).first()
            if not city:
                messages.error(request, 'شهر مورد نظر وجود ندارد')
                return redirect('dashboard')

            address.city_id = city
            address.detail = detail
            address.save()
            messages.success(request, 'ویرایش شما با موفقیت انجام شد')
            return redirect('dashboard')  
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)
    return redirect('dashboard')

@login_required
def delete_address(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    address = get_object_or_404(models.Addresses, pk=pk)
    if not address:
        messages.error(request, 'دسترسی غیرمجاز')
        return redirect('logout')
    else:
        if not address.user_id.id == request.user.id:
            messages.error(request, 'دسترسی غیرمجاز')
            return redirect('logout')
    address.delete()
    return redirect('dashboard')

@login_required
def delete_comment(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    comment = get_object_or_404(models.Comments, pk=pk)
    if not comment:
        messages.error(request, 'دسترسی غیرمجاز')
        return redirect('logout')
    else:
        if not comment.user_id.id == request.user.id:
            messages.error(request, 'دسترسی غیرمجاز')
            return redirect('logout')
    comment.delete()
    return redirect('dashboard')     
```
- ### Update urls.py File
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
    path('dashboard/update-profile', views.update_profile, name='update_profile'),
    path('dashboard/update-address/<int:pk>', views.update_address, name='update_address'),
    path('dashboard/delete-address/<int:pk>', views.delete_address, name='delete_address'),
    path('dashboard/delete-comment/<int:pk>', views.delete_comment, name='delete_comment'),
]
```
- ### In templates Folder, Update dashboard.html File
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
                {{ user.username }}
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
                            <th class="second">{{ user.username }}</th>
                        </tr>
                        <tr>
                            <th class="first">شماره تماس</th>
                            <th class="second">{{ user.phone }}</th>
                        </tr>
                        <tr>
                            <th class="first">پست الکترونیک</th>
                            <th class="second">{{ user.email }}</th>
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
                        {% if messages %}
                        <ul class="message-box">
                            {% for message in messages %}
                            <li class="alert alert-{{message.tags}}">{{message}}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        <form action="{% url 'update_profile' %}" autocomplete="on" method="post">
                            {% csrf_token %}
                            <input value="{{ user }}" type="text" name="username" placeholder="نام کاربری خود را وارد کنید">
                            <input value="{{ user.phone }}" type="text" name="phone" placeholder="شماره تماس خود را وارد کنید">
                            <input value="{{ user.email }}" type="text" name="email" placeholder="پست الکترونیک خود را وارد کنید">
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
                        {% for address in addresses %}
                        <tr>
                            <td>{{ address.id }}</td>
                            <td>{{ address.city_id.region_id.label }}</td>
                            <td>{{ address.city_id }}</td>
                            <td>{{ address.detail }}</td>
                            <td>
                                <button class="table-btn warning" onclick="openDialogBox('address-dialog-box-update-{{ address.id }}')">ویرایش</button>
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('address-dialog-box-delete-{{ address.id }}')">حذف</button>
                            </td>
                            <div class="address-dialog-box-update" id="address-dialog-box-update-{{ address.id }}">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-update-{{ address.id }}')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    {% if messages %}
                                    <ul class="message-box">
                                        {% for message in messages %}
                                        <li class="alert alert-{{message.tags}}">{{message}}</li>
                                        {% endfor %}
                                    </ul>
                                    {% endif %}
                                    <form action="{% url 'update_address' address.id %}" autocomplete="on" method="post">
                                        {% csrf_token %}
                                        <input value="{{ address.city_id.region_id.id }}" name="region_id" list="region" placeholder="استان خود را انتخاب کنید">
                                        <datalist id="region">
                                            {% for region in regions %}
                                            <option value="{{ region.id }}">{{ region.label }}</option>
                                            {% endfor %}
                                        </datalist>
                                        <input value="{{ address.city_id.id }}" name="city_id" list="city" placeholder="شهر خود را انتخاب کنید">
                                        <datalist id="city">
                                            {% for city in cities %}
                                            <option value="{{ city.id }}">{{ city.label }}</option>
                                            {% endfor %}
                                        </datalist>
                                        <input value="{{ address.detail }}" type="text" name="detail" placeholder="جزئیات آدرس خود را وارد کنید">
                                        <input type="submit" value="ارسال کن">
                                    </form>
                                </div>
                            </div>
                            <div class="address-dialog-box-delete" id="address-dialog-box-delete-{{ address.id }}">
                                <div class="close-box" onclick="closeDialogBox('address-dialog-box-delete-{{ address.id }}')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>آدرس مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن آدرس مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="{% url 'delete_address' address.id %}" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('address-dialog-box-delete-{{ address.id }}')">خیر</a>
                                </div>
                            </div>
                        </tr>
                        {% endfor %}
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
                        {% for comment in comments %}
                        <tr>
                            <td>{{ comment.id }}</td>
                            <td>{{ comment.product_id.label }}</td>
                            <td>{{ comment.description }}</td>
                            <td>
                                {% if comment.status == 1 %}
                                <button class="table-btn success">فعال</button>
                                {% else %}
                                <button class="table-btn danger">غیرفعال</button>
                                {% endif %}
                            </td>
                            <td>
                                <button class="table-btn danger" onclick="openDialogBox('comment-dialog-box-delete-{{ comment.id }}')">حذف</button>
                            </td>
                            <div class="comment-dialog-box-delete" id="comment-dialog-box-delete-{{ comment.id }}">
                                <div class="close-box" onclick="closeDialogBox('comment-dialog-box-delete-{{ comment.id }}')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <p>نظر مورد نظر پاک شود؟</p>
                                    <hr>
                                    <p>هشدار! در صورت پاک شدن نظر مورد نظر؛ امکان بازگشت وجود ندارد.</p>
                                    <hr>
                                    <a href="{% url 'delete_comment' comment.id %}" class="a-style danger confirm">آری</a>
                                    <a class="a-style success confirm" onclick="closeDialogBox('comment-dialog-box-delete-{{ comment.id }}')">خیر</a>
                                </div>
                            </div>
                        </tr>
                        {% endfor %}
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
                        {% for order in orders %}
                        <tr>
                            <td>{{ order.id }}</td>
                            <td>
                                {{ order.address_id.city_id.region_id.label }} - 
                                {{ order.address_id.city_id.label }} - 
                                {{ order.address_id.detail }}
                            </td>
                            <td>
                                {% if order.discount_id %}
                                {{ order.discount_id.label }}
                                {% else %}
                                تخفیف ندارد
                                {% endif %}
                            </td>
                            <td>{{ order.total_price }} ريال</td>
                            <td>{{ order.pay_price }} ريال</td>
                            <td>
                                <button class="table-btn info" onclick="openDialogBox('order-dialog-box-detail-{{ order.id }}')">محصولات</button>
                            </td>
                            <td>
                                {% if order.status == 1 %}
                                <button class="table-btn success">فعال</button>
                                {% else %}
                                <button class="table-btn danger">غیر فعال</button>
                                {% endif %}
                            </td>
                            <td>
                                {% if order.status == 1 %}
                                <button class="table-btn success">پرداخت شده</button>
                                {% else %}
                                <button class="table-btn warning"><a href="" style="text-decoration: none; color: inherit;">پرداخت</a></button>
                                {% endif %}
                            </td>
                            <div class="order-dialog-box-update" id="order-dialog-box-detail-{{ order.id }}">
                                <div class="close-box" onclick="closeDialogBox('order-dialog-box-detail-{{ order.id }}')">&#x2715;</div>
                                <div class="profile-dialog-box-content">
                                    <div class="product-title">
                                        <span class="product-title-item" style="width: 10%;">شناسه</span>
                                        <span class="product-title-item" style="width: 20%;">نام محصول</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ اصلی</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ با تخفیف</span>
                                        <span class="product-title-item" style="width: 10%;">تعداد</span>
                                        <span class="product-title-item" style="width: 20%;">مبلغ پرداخت شده</span>
                                    </div>
                                    {% for orderItem in order.order_list_item.all %}
                                    <div class="product-items">
                                        <span class="product-body-item" style="width: 10%;">{{ orderItem.id }}</span>
                                        <span class="product-body-item" style="width: 20%;">{{ orderItem.product_id.label }}</span>
                                        <span class="product-body-item" style="width: 20%;">{{ orderItem.total_price }} ريال</span>
                                        <span class="product-body-item" style="width: 20%;">{{ orderItem.pay_price }} ريال</span>
                                        <span class="product-body-item" style="width: 10%;">1</span>
                                        <span class="product-body-item" style="width: 20%;">{{ orderItem.pay_price }} ريال</span>
                                    </div> 
                                    {% endfor %} 
                                </div>
                            </div>
                        </tr>
                        {% endfor %}
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