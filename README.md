# Create Shop Project Bu Class View Structure

## <a href="https://github.com/pourghadiriHossein/Django/tree/session24">Download Shop Template</a>

## <a href="https://github.com/ali-zahedi/az-iranian-bank-gateways">Install azbankgateways</a>

```bash
pip install az-iranian-bank-gateways
```

## azbankgateways in site-packages
- ### Update admin.py File
```bash
from django.contrib import admin

from .models import Bank


class BankAdmin(admin.ModelAdmin):
    fields = [
        "user_id",
        "order_id",
        "pk",
        "status",
        "bank_type",
        "tracking_code",
        "amount",
        "reference_number",
        "response_result",
        "callback_url",
        "extra_information",
        "bank_choose_identifier",
        "created_at",
        "update_at",
    ]
    list_display = [
        "user_id",
        "order_id",
        "pk",
        "status",
        "bank_type",
        "tracking_code",
        "amount",
        "reference_number",
        "response_result",
        "callback_url",
        "extra_information",
        "bank_choose_identifier",
        "created_at",
        "update_at",
    ]
    list_filter = [
        "status",
        "bank_type",
        "created_at",
        "update_at",
    ]
    search_fields = [
        "status",
        "bank_type",
        "tracking_code",
        "amount",
        "reference_number",
        "response_result",
        "callback_url",
        "extra_information",
        "created_at",
        "update_at",
    ]
    exclude = []
    dynamic_raw_id_fields = []
    readonly_fields = [
        "pk",
        "status",
        "bank_type",
        "tracking_code",
        "amount",
        "reference_number",
        "response_result",
        "callback_url",
        "extra_information",
        "created_at",
        "update_at",
    ]


admin.site.register(Bank, BankAdmin)
```
- ### in models Update banks.py File
```bash
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from .enum import BankType, PaymentStatus


class BankQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super(BankQuerySet, self).__init__(*args, **kwargs)

    def active(self):
        return self.filter()


class BankManager(models.Manager):
    def get_queryset(self):
        return BankQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def update_expire_records(self):
        count = (
            self.active()
            .filter(
                status=PaymentStatus.RETURN_FROM_BANK,
                update_at__lte=datetime.datetime.now() - datetime.timedelta(minutes=15),
            )
            .update(status=PaymentStatus.EXPIRE_VERIFY_PAYMENT)
        )

        count = count + self.active().filter(
            status=PaymentStatus.REDIRECT_TO_BANK,
            update_at__lt=datetime.datetime.now() - datetime.timedelta(minutes=15),
        ).update(status=PaymentStatus.EXPIRE_GATEWAY_TOKEN)
        return count

    def filter_return_from_bank(self):
        return self.active().filter(status=PaymentStatus.RETURN_FROM_BANK)


class Bank(models.Model):
    #################################### Poulstar #################################
    user_id = models.ForeignKey(to='accounts.CustomUser', on_delete=models.CASCADE)
    order_id = models.ForeignKey(to='shop.Orders', on_delete=models.CASCADE)
    #################################### End Poulstar #################################

    status = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=PaymentStatus.choices,
        verbose_name=_("Status"),
    )
    bank_type = models.CharField(
        max_length=50,
        choices=BankType.choices,
        verbose_name=_("Bank"),
    )
    # It's local and generate locally
    tracking_code = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("Tracking code"))
    amount = models.CharField(max_length=10, null=False, blank=False, verbose_name=_("Amount"))
    # Reference number return from bank
    reference_number = models.CharField(
        unique=True,
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Reference number"),
    )
    response_result = models.TextField(null=True, blank=True, verbose_name=_("Bank result"))
    callback_url = models.TextField(null=False, blank=False, verbose_name=_("Callback url"))
    extra_information = models.TextField(null=True, blank=True, verbose_name=_("Extra information"))
    bank_choose_identifier = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Bank choose identifier")
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Created at"))
    update_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Updated at"))

    objects = BankManager()

    class Meta:
        verbose_name = _("Bank gateway")
        verbose_name_plural = _("Bank gateways")

    def __str__(self):
        return "{}-{}".format(self.pk, self.tracking_code)

    @property
    def is_success(self):
        return self.status == PaymentStatus.COMPLETE
```
- ### in banks folder Update banks.py File
```bash
import abc
import logging
import uuid
from urllib import parse

import six
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from .. import default_settings as settings
from ..exceptions import (
    AmountDoesNotSupport,
    BankGatewayStateInvalid,
    BankGatewayTokenExpired,
    CurrencyDoesNotSupport,
)
from ..models import Bank, CurrencyEnum, PaymentStatus
from ..utils import append_querystring


# TODO: handle and expire record after 15 minutes
@six.add_metaclass(abc.ABCMeta)
class BaseBank:
    """Base bank for sending to gateway."""

    _gateway_currency: str = CurrencyEnum.IRR
    _currency: str = CurrencyEnum.IRR
    _amount: int = 0
    _user_id = 0
    _order_id = 0
    _gateway_amount: int = 0
    _mobile_number: str = None
    _tracking_code: int = None
    _reference_number: str = ""
    _transaction_status_text: str = ""
    _client_callback_url: str = ""
    _bank: Bank = None
    _request = None

    def __init__(self, identifier: str, **kwargs):
        self.identifier = identifier
        self.default_setting_kwargs = kwargs
        self.set_default_settings()

    @abc.abstractmethod
    def set_default_settings(self):
        """default setting, like fetch merchant code, terminal id and etc"""
        pass

    def prepare_amount(self):
        """prepare amount"""
        if self._currency == self._gateway_currency:
            self._gateway_amount = self._amount
        elif self._currency == CurrencyEnum.IRR and self._gateway_currency == CurrencyEnum.IRT:
            self._gateway_amount = CurrencyEnum.rial_to_toman(self._amount)
        elif self._currency == CurrencyEnum.IRT and self._gateway_currency == CurrencyEnum.IRR:
            self._gateway_amount = CurrencyEnum.toman_to_rial(self._amount)
        else:
            self._gateway_amount = self._amount

        if not self.check_amount():
            raise AmountDoesNotSupport()

    def check_amount(self):
        return self.get_gateway_amount() >= self.get_minimum_amount()

    @classmethod
    def get_minimum_amount(cls):
        return 1000

    @abc.abstractmethod
    def get_bank_type(self):
        pass

    def get_amount(self):
        """get the amount"""
        return self._amount

    def get_user_id(self):
        """get the user id"""
        return self._user_id

    def get_order_id(self):
        """get the order id"""
        return self._order_id

    def set_amount(self, amount):
        """set amount"""
        if int(amount) <= 0:
            raise AmountDoesNotSupport()
        self._amount = int(amount)

    def set_user_id(self, user_id):
        """set user id"""
        try:
            self._user_id = user_id
        except:
            raise Exception("Pourghadiri")

    def set_order_id(self, order_id):
        """set order id"""
        try:
            self._order_id = order_id
        except:
            raise Exception("Pourghadiri 2")

    @abc.abstractmethod
    def prepare_pay(self):
        logging.debug("Prepare pay method")
        self.prepare_amount()
        tracking_code = int(str(uuid.uuid4().int)[-1 * settings.TRACKING_CODE_LENGTH :])
        self._set_tracking_code(tracking_code)

    @abc.abstractmethod
    def get_pay_data(self):
        pass

    @abc.abstractmethod
    def pay(self):
        logging.debug("Pay method")
        self.prepare_pay()

    @abc.abstractmethod
    def get_verify_data(self):
        pass

    @abc.abstractmethod
    def prepare_verify(self, tracking_code):
        logging.debug("Prepare verify method")
        self._set_tracking_code(tracking_code)
        self._set_bank_record()
        self.prepare_amount()

    @abc.abstractmethod
    def verify(self, tracking_code):
        logging.debug("Verify method")
        self.prepare_verify(tracking_code)

    def ready(self) -> Bank:
        self.pay()
        bank = Bank.objects.create(
            bank_choose_identifier=self.identifier,
            bank_type=self.get_bank_type(),
            amount=self.get_amount(),
            user_id=self.get_user_id(),
            order_id=self.get_order_id(),
            reference_number=self.get_reference_number(),
            response_result=self.get_transaction_status_text(),
            tracking_code=self.get_tracking_code(),
        )
        self._bank = bank
        self._set_payment_status(PaymentStatus.WAITING)
        if self._client_callback_url:
            self._bank.callback_url = self._client_callback_url
        return bank

    @abc.abstractmethod
    def prepare_verify_from_gateway(self):
        pass

    def verify_from_gateway(self, request):
        """زمانی که کاربر از گیت وی بانک باز میگردد این متد فراخوانی می شود."""
        self.set_request(request)
        self.prepare_verify_from_gateway()
        self._set_payment_status(PaymentStatus.RETURN_FROM_BANK)
        self.verify(self.get_tracking_code())

    def get_client_callback_url(self):
        """این متد پس از وریفای شدن استفاده خواهد شد. لینک برگشت را بر میگرداند.حال چه وریفای موفقیت آمیز باشد چه با
        لغو کاربر مواجه شده باشد"""
        return append_querystring(
            self._bank.callback_url,
            {settings.TRACKING_CODE_QUERY_PARAM: self.get_tracking_code()},
        )

    def redirect_client_callback(self):
        """ "این متد کاربر را به مسیری که نرم افزار میخواهد هدایت خواهد کرد و پس از وریفای شدن استفاده می شود."""
        logging.debug("Redirect to client")
        return redirect(self.get_client_callback_url())

    def set_mobile_number(self, mobile_number):
        """شماره موبایل کاربر را جهت ارسال به درگاه برای فتچ کردن شماره کارت ها و ... ارسال خواهد کرد."""
        self._mobile_number = mobile_number

    def get_mobile_number(self):
        return self._mobile_number

    def set_client_callback_url(self, callback_url):
        """ذخیره کال بک از طریق نرم افزار برای بازگردانی کاربر پس از بازگشت درگاه بانک به پکیج و سپس از پکیج به نرم
        افزار."""
        if not self._bank:
            self._client_callback_url = callback_url
        else:
            logging.critical(
                "You are change the call back url in invalid situation.",
                extra={
                    "bank_id": self._bank.pk,
                    "status": self._bank.status,
                },
            )
            raise BankGatewayStateInvalid(
                "Bank state not equal to waiting. Probably finish "
                f"or redirect to bank gateway. status is {self._bank.status}"
            )

    def _set_reference_number(self, reference_number):
        """reference number get from bank"""
        self._reference_number = reference_number

    def _set_bank_record(self):
        try:
            self._bank = Bank.objects.get(
                Q(Q(reference_number=self.get_reference_number()) | Q(tracking_code=self.get_tracking_code())),
                Q(bank_type=self.get_bank_type()),
            )
            logging.debug("Set reference find bank object.")
        except Bank.DoesNotExist:
            logging.debug("Cant find bank record object.")
            raise BankGatewayStateInvalid(
                "Cant find bank record with reference number reference number is {}".format(
                    self.get_reference_number()
                )
            )
        self._set_tracking_code(self._bank.tracking_code)
        self._set_reference_number(self._bank.reference_number)
        self.set_amount(self._bank.amount)
        self.set_user_id(self._bank.user_id)
        self.set_order_id(self._bank.order_id)

    def get_reference_number(self):
        return self._reference_number

    """
    ترنزکشن تکست متنی است که از طرف درگاه بانک به عنوان پیام باز میگردد.
    """

    def _set_transaction_status_text(self, txt):
        self._transaction_status_text = txt

    def get_transaction_status_text(self):
        return self._transaction_status_text

    def _set_payment_status(self, payment_status):
        if payment_status == PaymentStatus.RETURN_FROM_BANK and self._bank.status != PaymentStatus.REDIRECT_TO_BANK:
            logging.debug(
                "Payment status is not status suitable.",
                extra={"status": self._bank.status},
            )
            raise BankGatewayStateInvalid(
                "You change the status bank record before/after this record change status from redirect to bank. "
                "current status is {}".format(self._bank.status)
            )
        self._bank.status = payment_status
        self._bank.save()
        logging.debug("Change bank payment status", extra={"status": payment_status})

    def set_gateway_currency(self, currency: CurrencyEnum):
        """واحد پولی درگاه بانک"""
        if currency not in [CurrencyEnum.IRR, CurrencyEnum.IRT]:
            raise CurrencyDoesNotSupport()
        self._gateway_currency = currency

    def get_gateway_currency(self):
        return self._gateway_currency

    def set_currency(self, currency: CurrencyEnum):
        """ "واحد پولی نرم افزار"""
        if currency not in [CurrencyEnum.IRR, CurrencyEnum.IRT]:
            raise CurrencyDoesNotSupport()
        self._currency = currency

    def get_currency(self):
        return self._currency

    def get_gateway_amount(self):
        return self._gateway_amount

    """
    ترکینگ کد توسط برنامه تولید شده و برای استفاده های بعدی کاربرد خواهد داشت.
    """

    def _set_tracking_code(self, tracking_code):
        self._tracking_code = tracking_code

    def get_tracking_code(self):
        return self._tracking_code

    """ًRequest"""

    def set_request(self, request):
        self._request = request

    def get_request(self):
        return self._request

    """gateway"""

    def _prepare_check_gateway(self, amount=None, user_id=None, order_id=None):
        """ست کردن داده های اولیه"""
        if amount and user_id and order_id:
            self.set_amount(amount)
            self.set_user_id(user_id)
            self.set_order_id(order_id)
        else:
            self.set_amount(10000)
            self.set_user_id(1)
            self.set_order_id(1)
        self.set_client_callback_url("/")

    def check_gateway(self, amount=None):
        """با این متد از صحت و سلامت گیت وی برای اتصال اطمینان حاصل می کنیم."""
        self._prepare_check_gateway(amount)
        self.pay()

    @abc.abstractmethod
    def _get_gateway_payment_url_parameter(self):
        """این متد بسته به بانک متفاوت پر می شود."""
        """
        :return
        url: str
        """
        pass

    @abc.abstractmethod
    def _get_gateway_payment_parameter(self):
        """این متد بسته به بانک متفاوت پر می شود."""
        """
        :return
        params: dict
        """
        pass

    @abc.abstractmethod
    def _get_gateway_payment_method_parameter(self):
        """این متد بسته به بانک متفاوت پر می شود."""
        """
        :return
        method: POST, GET
        """
        pass

    def redirect_gateway(self):
        """کاربر را به درگاه بانک هدایت می کند"""
        if (timezone.now() - self._bank.created_at).seconds > 120:
            self._set_payment_status(PaymentStatus.EXPIRE_GATEWAY_TOKEN)
            logging.debug("Redirect to bank expire!")
            raise BankGatewayTokenExpired()
        logging.debug("Redirect to bank")
        self._set_payment_status(PaymentStatus.REDIRECT_TO_BANK)
        return redirect(self.get_gateway_payment_url())

    def get_gateway_payment_url(self):
        redirect_url = reverse(settings.GO_TO_BANK_GATEWAY_NAMESPACE)
        url = self._get_gateway_payment_url_parameter()
        params = self._get_gateway_payment_parameter()
        method = self._get_gateway_payment_method_parameter()
        params.update(
            {
                "url": url,
                "method": method,
            }
        )
        redirect_url = append_querystring(redirect_url, params)
        if self.get_request():
            redirect_url = self.get_request().build_absolute_uri(redirect_url)
        return redirect_url

    def _get_gateway_callback_url(self):
        url = reverse(settings.CALLBACK_NAMESPACE)
        if self.get_request():
            url_parts = list(parse.urlparse(url))
            if not (url_parts[0] and url_parts[1]):
                url = self.get_request().build_absolute_uri(url)
            query = dict(parse.parse_qsl(self.get_request().GET.urlencode()))
            query.update({"bank_type": self.get_bank_type()})
            query.update({"identifier": self.identifier})
            url = append_querystring(url, query)

        return url
```

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

## Create app transaction
### In Windows
```bash
py manage.py startapp transaction
```
### In MacOS
```bash
python manage.py startapp transaction
```
### In Linux
```bash
python3 manage.py startapp transaction
```
## Create static folder then copy CSS, FONT, IMAGE, JS Folder from downloaded template to it

## Create templates Folder in Root Directory
- ### Create publicLayout.html File
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
- ### Create registration Folder
- ### In registration Foder, Create login.html File
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
        {% if messages %}
        <ul class="message-box">
            {% for message in messages %}
            <li class="alert alert-{{message.tags}}">{{message}}</li>
            {% endfor %}
        </ul>
        {% endif %}
        <form action="{% url 'login' %}" method="POST" autocomplete="on">
            {% csrf_token %}
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
- ### In registration Foder, Create signup.html File
```bsah
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
        {% if messages %}
        <ul class="message-box">
            {% for message in messages %}
            <li class="alert alert-{{message.tags}}">{{message}}</li>
            {% endfor %}
        </ul>
        {% endif %}
        <form action="{% url 'sign_up' %}" method="POST" autocomplete="on">
            {% csrf_token %}
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
## Create lib Folder
- ### Create error_handling.py File
```bash
def error_progres(errors):
    error_messages = []    
    for error in errors:
        error_messages.append(errors[error][0])
    return error_messages
```
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
- ### Create __init__.py File
```bash
from lib.error_handling import *
from lib.session import *
```
## In session app 
- ### Update views.py File
```bash
from django.shortcuts import redirect
from shop.models import Discounts
from django.views import View

class AddToSession(View):
    def get(self, request, pk):
        flag_for_Loop = True
        quantity = 1
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
    def post(self, request, pk):
        flag_for_Loop = True
        quantity = 1
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

class MinesFromSession(View):
    def get(self, request, pk):
        if 'cart' in request.session:
            for item in request.session['cart']:
                if item[0] == pk:
                    if request.session['cart'][request.session['cart'].index(item)][1] > 1:
                        request.session['cart'][request.session['cart'].index(item)][1] -= 1
                    else:
                        del request.session['cart'][request.session['cart'].index(item)]

        request.session.modified = True
        return redirect(request.META.get("HTTP_REFERER"))

class PlusFromSession(View):
    def get(self, request, pk):
        if 'cart' in request.session:
            for item in request.session['cart']:
                if item[0] == pk:
                    request.session['cart'][request.session['cart'].index(item)][1] += 1  

        request.session.modified = True
        return redirect(request.META.get("HTTP_REFERER"))

class DeleteItemFromSession(View):
    def get(self, request, pk):
        if 'cart' in request.session:
            for item in request.session['cart']:
                if item[0] == pk:
                    del request.session['cart'][request.session['cart'].index(item)]

        request.session.modified = True
        return redirect(request.META.get("HTTP_REFERER"))

class AddDiscountToSession(View):
    def get(self, request, pk):
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
    path('add-to-session/<int:pk>/', views.AddToSession.as_view(), name='add_to_session'),
    path('mines-from-session/<int:pk>/', views.MinesFromSession.as_view(), name='mines_from_session'),
    path('plus-from-session/<int:pk>/', views.PlusFromSession.as_view(), name='plus_from_session'),
    path('delete-item-from-session/<int:pk>/', views.DeleteItemFromSession.as_view(), name='delete_item_from_session'),
    path('add-discount/', views.AddToSession.as_view(), name='add_discount'),
]
```
## In shop app
- ### Create templatetags Folder
- ### In templatetags, Create tools.py File
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
- ### In templatetags, Create __init__.py File

- ### Create templates Folder then Create dashboard and public Folder in it
- ### In templates/dashboard Folder, Create dashboard.html File
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
                                <button class="table-btn warning"><a href="{% url 'start_getway' order.pay_price|showPrice order.user_id.phone order.id %}" style="text-decoration: none; color: inherit;">پرداخت</a></button>
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
                            <th>بانک انتخابی</th>
                            <th>مبلغ پرداخت شده</th>
                            <th>کد رهگیری</th>
                            <th>شناسه رهگیری</th>
                            <th>تاریخ پرداخت</th>
                            <th>تاریخ تایید پرداخت</th>
                            <th>وضعیت</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for transaction in transactions %}
                        <tr>
                            <td>{{ transaction.pk }}</td>
                            <td>{{ transaction.order_id.id }}</td>
                            <td>{{ transaction.bank_type }}</td>
                            <td>{{ transaction.amount }} ريال</td>
                            <td>{{ transaction.tracking_code }}</td>
                            <td>{{ transaction.reference_number }}</td>
                            <td style="direction: ltr;">{{ transaction.created_at }}</td>
                            <td style="direction: ltr;">{{ transaction.update_at }}</td>
                            <td>
                                {% if transaction.status == 'Complete' %}
                                <button class="table-btn success">موفق</button>
                                {% else %}
                                <button class="table-btn danger">ناموفق</button>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>

</body>
</html>
```
- ### In templates/public Folder, Create cart.html File
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
- ### In templates/public Folder, Create checkout.html File
```bash
{% extends 'publicLayout.html' %}
{% load static %}
{% block css %}
{% load tools %}
<link rel="stylesheet" href="{% static 'CSS/Checkout.css' %}">
{% endblock %}

{% block content %}
<div class="mainBox checkout">
    {% if messages %}
        <ul class="message-box">
            {% for message in messages %}
            <li class="alert alert-{{message.tags}}">{{message}}</li>
            {% endfor %}
        </ul>
    {% endif %}
    <form action="{% url 'checkout' %}" method="POST" autocomplete="on">
        {% csrf_token %}
        <div class="partition">
            <div class="previousAddress">
                <label><input type="checkbox" name="previousAddress">&nbsp; آردس پیش فرض &nbsp;</label>
                
                {% for address in user_address %}
                <label><input type="radio" value="{{ address.id }}" name="selectedPreviousAddress"> 
                    {{ address.city_id.region_id.label }} -  
                    {{ address.city_id.label }} -  
                    {{ address.detail }}
                </label>
                {% endfor %}
            </div>
            <div class="newAddress">
                <label><input type="checkbox" name="newAddress">&nbsp; آردس جدید &nbsp;</label>
                <input list="region" name="selectedNewAddress" placeholder="کد شهر خود را انتخاب کنید"> 
                <datalist id="region">
                    {% for city in cities %}
                    <option value="{{ city.id }}">{{ city }}</option>
                    {% endfor %}
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
                <input type="checkbox" name="acceptTerm">
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
- ### In templates/public Folder, Create contact.html File
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
- ### In templates/public Folder, Create frequencyAndAnswer.html.html File
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
- ### In templates/public Folder, Create home.html.html File
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
- ### In templates/public Folder, Create product.html.html File
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
- ### In templates/public Folder, Create singleProduct.html.html File
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
- ### In templates/public Folder, Create termAndCondition.html.html File
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
        return f"{self.id}"

class OrderListItems (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE, related_name='order_list_item')
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    pay_price = models.DecimalField(max_digits=20, decimal_places=2)
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
```
- ### Update views.py File
```bash
from django.shortcuts import get_object_or_404, redirect
from django.urls import resolve
from . import models
from accounts.models import CustomUser
from django.contrib import messages
from .forms import Update_Profile, Update_Address, Checkout
from lib import error_progres, get_cart_session, get_discount_session, clear_session
from azbankgateways.models import Bank
from django.views import generic ,View
from django.contrib.auth.mixins import LoginRequiredMixin

class CartView(generic.ListView):        
    model = models.Tags
    template_name = 'public/cart.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        final_cart_lists, total_price = get_cart_session(request)
        total_discount = get_discount_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
            'total_price' : total_price,
            'total_discount' : total_discount,
        }
        CartView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class CheckoutView(LoginRequiredMixin, generic.ListView):        
    model = models.Tags
    template_name = 'public/checkout.html'
    
    def dispatch(self, request, *args, **kwargs):
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
            return redirect(request.META.get("HTTP_REFERER"))
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        user_address = models.Addresses.objects.filter(user_id=request.user.id)
        cities = models.Cities.objects.all()
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
            'total_price' : total_price,
            'total_discount' : total_discount,
            'user_address' : user_address,
            'cities' : cities,
        }
        CheckoutView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class ContactView(generic.ListView):        
    model = models.Tags
    template_name = 'public/contact.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
        }
        ContactView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class FAQView(generic.ListView):        
    model = models.Tags
    template_name = 'public/frequencyAndAnswer.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
        }
        FAQView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class HomeView(generic.ListView):        
    model = models.Tags
    template_name = 'public/home.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        
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
        extra_context = {
            'urlName': current_url,
            'categories' : mainCategories,
            'latestProduct' : latestProduct,
            'latestMenProduct' : latestMenProduct,
            'latestWomenProduct' : latestWomenProduct,
            'final_cart_lists': final_cart_lists,
        }
        HomeView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)


class ProductView(generic.ListView):        
    model = models.Tags
    template_name = 'public/product.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        current_category = get_object_or_404(models.Categories, pk = self.kwargs['pk'])
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
            if category.id == self.kwargs['pk'] or (category.parent_id != None and category.parent_id.id == self.kwargs['pk']):
                category_IDs.append(category.id)
        products = models.Products.objects.filter(category_id__in=category_IDs).order_by('-id')
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'current_category' : current_category,
            'tag' : False,
            'tags' : tags,
            'latestMenProduct' : latestMenProduct,
            'latestWomenProduct' : latestWomenProduct,
            'products' : products,
            'final_cart_lists': final_cart_lists,
        }
        ProductView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)


class TagView(generic.ListView):        
    model = models.Tags
    template_name = 'public/product.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        current_tag = get_object_or_404(models.Tags, pk = self.kwargs['pk'])
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
        products = models.Products.objects.filter(tag_id=self.kwargs['pk']).order_by('-id')
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'current_category' : False,
            'tag' : current_tag,
            'tags' : tags,
            'latestMenProduct' : latestMenProduct,
            'latestWomenProduct' : latestWomenProduct,
            'products' : products,
            'final_cart_lists': final_cart_lists,
        }
        TagView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class SingleProductView(generic.ListView):        
    model = models.Tags
    template_name = 'public/singleProduct.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        product = get_object_or_404(models.Products, pk = self.kwargs['pk'])
        comments = models.Comments.objects.filter(product_id=self.kwargs['pk'])
        latestProduct = models.Products.objects.order_by('-id')[:3]
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'product' : product,
            'comments' : comments,
            'latestProduct' : latestProduct,
            'final_cart_lists': final_cart_lists,
        }
        SingleProductView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)
        

class TACView(generic.ListView):        
    model = models.Tags
    template_name = 'public/termAndCondition.html'
    
    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        categories = models.Categories.objects.filter(parent_id = None)
        final_cart_lists, total_price = get_cart_session(request)
        extra_context = {
            'urlName': current_url,
            'categories' : categories,
            'final_cart_lists': final_cart_lists,
        }
        TACView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, generic.ListView):        
    model = models.Regions
    template_name = 'dashboard/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        user_addresses = models.Addresses.objects.filter(user_id=request.user.id)
        cities = models.Cities.objects.all()
        user_comments = models.Comments.objects.filter(user_id=request.user.id)
        user_orders = models.Orders.objects.filter(user_id=request.user.id)
        transactions = Bank.objects.filter(user_id=request.user.id)
        extra_context = {
            'addresses' : user_addresses,
            'cities' : cities,
            'comments' : user_comments,
            'orders' : user_orders,
            'transactions' : transactions,
        }
        DashboardView.extra_context = extra_context
        return super().dispatch(request, *args, **kwargs)

class UpdateProfileView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
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

class UpdateAddressView(LoginRequiredMixin, View):
    def post(self, request, pk):
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

class DeleteAddressView(LoginRequiredMixin, View):
    def get(self, request, pk):
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

class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, pk):
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

- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('frequency-and-answer/', views.FAQView.as_view(), name='faq'),
    path('<int:pk>/product/', views.ProductView.as_view(), name='product'),
    path('<int:pk>/tag/', views.TagView.as_view(), name='tag'),
    path('<int:pk>/single-product/', views.SingleProductView.as_view(), name='singleProduct'),
    path('term-and-condition/', views.TACView.as_view(), name='tac'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/update-profile', views.UpdateProfileView.as_view(), name='update_profile'),
    path('dashboard/update-address/<int:pk>', views.UpdateAddressView.as_view(), name='update_address'),
    path('dashboard/delete-address/<int:pk>', views.DeleteAddressView.as_view(), name='delete_address'),
    path('dashboard/delete-comment/<int:pk>', views.DeleteCommentView.as_view(), name='delete_comment'),
]
```
## In accounts app
- ### Update models.py File
```bash
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=14, unique=True, null=True, blank=True)
    status = models.SmallIntegerField(default=1)
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
- ### Create forms.py File
```bash
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
```
- ### Update views.py File
```bash
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
```
- ### Create urls.py File
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
```
## In transaction app
- ### Update views.py File
```bash
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from shop.models import Orders

@login_required
def go_to_gateway_view(request, price, phone, order):
    amount = int(price)
    user_mobile_number = str(phone) 
    order_id = get_object_or_404(Orders, pk=order)

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_user_id(request.user)
        bank.set_order_id(order_id)
        bank.set_client_callback_url(reverse('call-back'))
        bank.set_mobile_number(user_mobile_number)
    
        bank_record = bank.ready()
        
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    if bank_record.is_success:
        messages.success(request,'پرداخت با موفقیت انجام شد')
        order = bank_record.order_id
        order.status = True
        order.save()
        return redirect('dashboard')

    messages.error(request,'پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت')
    return redirect('dashboard')
```

## In config Folder
- ### Update settings.py File
```bash
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l2*#e_vzm#5)#r^mr95s6c_de@v-ccqi^laldio&^2zfe9ca03'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

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
    'azbankgateways',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]

MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "home"

IDPAY_MERCHANT_CODE = '6a7f99eb-7c20-4412-a972-6dfb7cd253a4'

AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'IDPAY': {
           'MERCHANT_CODE': IDPAY_MERCHANT_CODE,
           'METHOD': 'POST', 
           'X_SANDBOX': 1, 
       },
   },
   'IS_SAMPLE_FORM_ENABLE': True,
   'DEFAULT': 'IDPAY',
   'CURRENCY': 'IRR',
   'TRACKING_CODE_QUERY_PARAM': 'tc',
   'TRACKING_CODE_LENGTH': 16, 
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader', 
   'BANK_PRIORITIES': [
   ],
}
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```
- ### Update urls.py File
```bash
"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls
from transaction.views import go_to_gateway_view, callback_gateway_view

admin.autodiscover() 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('accounts/', include('accounts.urls')),
    path('session/', include('session.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-getway/<int:price>/<str:phone>/<int:order>/', go_to_gateway_view, name='start_getway'),
    path('call-back/', callback_gateway_view, name='call-back'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Make Migrations for Project
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