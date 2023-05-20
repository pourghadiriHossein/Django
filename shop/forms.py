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
    
class Checkout(forms.Form):
    previousAddress = forms.CharField(required=False)
    selectedPreviousAddress = forms.CharField(required=False)
    newAddress = forms.CharField(required=False)
    selectedNewAddress = forms.CharField(required=False)
    detail = forms.CharField(required=False, min_length=4, max_length=1000,
    error_messages={
        'min_length' : 'جزئیات آدرس شما نمی تواند کمتر از 4 کاراکتر باشد',
        'max_length' : 'جزئیات آدرس شما نمی تواند بیشتر از 1000 کاراکتر باشد',
    })
    acceptTerm = forms.CharField(required=True,
    error_messages={
        'required' : 'برای ادامه فرآیند، باید قوانین و مقررات را بپذیرید',
    })
    
    def clean(self):
        data = self.cleaned_data
        if data.get('previousAddress', None):
            if data.get('selectedPreviousAddress', None):
                return data
            else:
                raise forms.ValidationError('یکی از آدرس های پیش فرض خود را انتخاب کنید')
        elif data.get('newAddress', None):
            if data.get('selectedNewAddress', None) and data.get('detail', None):
                return data
            else:
                raise forms.ValidationError('یا شهر انتخاب نکرده اید یا جزئیات آدرس را ننوشته اید')
        else:
            raise forms.ValidationError('آدرس خود را مشخص کنید، اگر آدرس قدیم خود را انتخاب می کنید ، حتما تیک آدرس پیش فرض را بزنید و اگر آدرس جدید پر می کنید، حتما تیک آدرس جدید را بزنید')