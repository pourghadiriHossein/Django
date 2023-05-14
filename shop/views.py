from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve
from . import models
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from django.contrib import messages
from .forms import Update_Profile, Update_Address, Checkout
from lib import error_progres, get_cart_session, get_discount_session, clear_session
from azbankgateways.models import Bank

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

@login_required
def checkout(request):
    final_cart_lists, total_price = get_cart_session(request)
    total_discount = get_discount_session(request)
    if request.method == 'POST':
        form = Checkout(request.POST)
        if form.is_valid():
            if request.POST.get('selectedPreviousAddress'):
                selectedPreviousAddress = request.POST.get('selectedPreviousAddress')
                address_for_order = get_object_or_404(models.Addresses, pk=selectedPreviousAddress)
            elif request.POST.get('selectedNewAddress'):    
                selectedNewAddress = request.POST.get('selectedNewAddress')
                city = get_object_or_404(models.Cities, pk=selectedNewAddress)
                detail = request.POST.get('detail')
                address_for_order = models.Addresses.objects.create(
                    city_id = city,
                    user_id = request.user,
                    detail = detail,
                )
            if total_discount:
                if total_discount > 0:
                    cal_pay_price = total_price - total_discount
                    discount_for_order = models.Discounts.objects.filter(price=total_discount).first()
                    order_for_order_list = models.Orders.objects.create(
                        user_id = request.user,
                        address_id = address_for_order,
                        discount_id = discount_for_order,
                        total_price = total_price,
                        pay_price = cal_pay_price,
                        status = False,
                    )
            else:
                order_for_order_list = models.Orders.objects.create(
                    user_id = request.user,
                    address_id = address_for_order,
                    total_price = total_price,
                    pay_price = total_price,
                    status = False,
                )
            for item in final_cart_lists:
                total_price = item['cart_product'].price * item['quantity']
                if item['cart_product'].discount_id:
                    if item['cart_product'].discount_id.price:
                        cal_price = item['cart_product'].price - item['cart_product'].discount_id.price
                        pay_price = cal_price * item['quantity']
                    elif item['cart_product'].discount_id.percent:
                        computed_price = item['cart_product'].price * item['cart_product'].discount_id.percent/100
                        price = item['cart_product'].price - computed_price
                        pay_price = price * item['quantity']
                else:
                    pay_price = total_price
                models.OrderListItems.objects.create(
                    user_id = request.user,
                    product_id = item['cart_product'],
                    order_id = order_for_order_list,
                    total_price = total_price,
                    pay_price = pay_price,
                    status = True
                )
            clear_session(request,'cart')
            if total_discount > 0:
                clear_session(request, 'discount')
            return redirect('start_getway', int(order_for_order_list.pay_price), request.user.phone, order_for_order_list.id)
        else:
            error_messages = error_progres(form.errors)
            for error in error_messages:
                messages.error(request, error)
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    user_address = models.Addresses.objects.filter(user_id=request.user.id)
    cities = models.Cities.objects.all()
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'final_cart_lists': final_cart_lists,
        'total_price' : total_price,
        'total_discount' : total_discount,
        'user_address' : user_address,
        'cities' : cities,
    }
    return render(request, 'public/checkout.html', context)

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

@login_required
def dashboard(request):
    user_addresses = models.Addresses.objects.filter(user_id=request.user.id)
    regions = models.Regions.objects.all()
    cities = models.Cities.objects.all()
    user_comments = models.Comments.objects.filter(user_id=request.user.id)
    user_orders = models.Orders.objects.filter(user_id=request.user.id)
    transactions = Bank.objects.filter(user_id=request.user.id)
    context = {
        'addresses' : user_addresses,
        'regions' : regions,
        'cities' : cities,
        'comments' : user_comments,
        'orders' : user_orders,
        'transactions' : transactions,
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