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
    discount_id = models.ForeignKey(to=Discounts, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    pay_price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField()

    def __str__(self):
        return self.user_id.name

class OrderListItems (models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField()

    def __str__(self):
        return self.user_id.name