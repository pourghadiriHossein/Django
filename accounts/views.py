from django.shortcuts import redirect
from django.urls import resolve
from shop import models
from django.contrib.auth import authenticate, login, logout
from .forms import Login, SignUp
from django.contrib import messages
from .models import CustomUser
from lib import error_progres, get_cart_session
from django.views import generic, View

class LoginView(generic.ListView):        
    model = models.Tags
    template_name = 'registration/login.html'
    
    def dispatch(self, request, *args, **kwargs):
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
                        login(request, login_user)
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'رمز عبور صحیح نیست')   
                else:
                    messages.error(request, 'کاربری با این شماره تماس وجود ندارد')
            else:
                error_messages = error_progres(form.errors)
                for error in error_messages:
                    messages.error(request, error)
            return redirect(request.META.get("HTTP_REFERER"))    

        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
        }
        LoginView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class SignUpView(generic.ListView):        
    model = models.Tags
    template_name = 'registration/signup.html'
    
    def dispatch(self, request, *args, **kwargs):
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
                    login(request, new_user)
                    return redirect('dashboard')
            else:
                error_messages = error_progres(form.errors)
                for error in error_messages:
                    messages.error(request, error)
            return redirect(request.META.get("HTTP_REFERER"))
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
        }
        LoginView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')
        else:
            return redirect('login')
