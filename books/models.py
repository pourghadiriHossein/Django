from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Book(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='عنوان')
    author = models.CharField(max_length=100, verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='قیمت')
    cover = models.ImageField(upload_to="covers/", verbose_name='عکس جلد', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])

class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name="نام کتاب")
    text = models.TextField(verbose_name="متن پیام")
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    recommend = models.BooleanField(default=True, verbose_name="پیشنهاد می شود")

    def __str__(self):
        return f"{self.user}: {self.text}"
