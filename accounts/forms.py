from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('phone', 'status')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class Login(forms.Form):
    phone = forms.CharField(required=True, min_length=11, max_length=14,
    error_messages={
        'required' : 'شماره تماس خود را وارد کنید',
        'min_length' : 'شماره تماس شما نمی تواند کمتر از 11 کاراکتر باشد',
        'max_length' : 'شماره تماس شما نمی تواند بیشتر از 14 کاراکتر باشد',
    })
    password = forms.CharField(required=True, min_length=4, max_length=100,
    error_messages={
        'required' : 'رمز عبور خود را وارد کنید',
        'min_length' : 'رمز عبور شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'رمز عبور شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })

class SignUp(forms.Form):
    name = forms.CharField(required=True, min_length=4, max_length=100,
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
    password = forms.CharField(required=True, min_length=4, max_length=100,
    error_messages={
        'required' : 'رمز عبور خود را وارد کنید',
        'min_length' : 'رمز عبور شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'رمز عبور شما نمی تواند بیشتر از 100 کاراکتر باشد',
    })    