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