# Complete Session Part In Shop Project

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

## Make Migrations Your App
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

## Migrate Your App
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

## config Folder
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
    'azbankgateways',
]
```
```bash
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
## Create transaction App
- ### In Windows
```bash
py manage.py startapp transaction
```
- ### In MacOS
```bash
python manage.py startapp transaction
```
- ### In Linux
```bash
python3 manage.py startapp transaction
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

- ### Update urls.py File
```bash
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

## In Shop App
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
- ### In templates Folder, In dashboard Folder, Update dashboard.html File 
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
- ### Update Orders model in models.py File
```bash
class Orders (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address_id = models.ForeignKey(to=Addresses, on_delete=models.CASCADE)
    discount_id = models.ForeignKey(to=Discounts, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    pay_price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField()

    def __str__(self):
        return f"{self.id}"
```
- ### Create Checkout class in forms.py File
```bash
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
from .forms import Update_Profile, Update_Address, Checkout
from lib import error_progres, get_cart_session, get_discount_session, clear_session
from azbankgateways.models import Bank
```
```bash
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
```
```bash
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