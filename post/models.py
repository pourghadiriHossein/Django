from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='upload')
    creator = models.CharField(max_length=40)
    create_at = models.DateTimeField()

    def __str__(self):
        return f"Post Title is: {self.title}"

    # boolean = models.BooleanField()
    # real_age = models.PositiveIntegerField()
    # float_age = models.FloatField()
    # slug = models.SlugField()
    # time = models.TimeField()
    # birth_day = models.DateField()
    # ip = models.GenericIPAddressField()
    # email = models.EmailField()
    # url = models.URLField()
    # image = models.ImageField() # اگه ننویسیم مستقیم تو خود پوشه اپ آپلود میکنه.
    # image = models.ImageField(upload_to='media')
    # file_field_test = models.FileField() # اگه ننویسیم مستقیم تو خود پوشه اپ آپلود میکنه.
    # file_field_test = models.FileField(upload_to='file haye man')
    # register_date = models.DateTimeField(auto_now_add=True)
    # registeration_update_date = models.DateTimeField(auto_now=True)
    # blank_name = models.CharField(max_length=50, blank=True) # blank is for validation
    # null_name = models.CharField(max_length=50, null=True) # null is db related
    # blank_null_name = models.CharField(max_length=50, blank=True, null=True)

