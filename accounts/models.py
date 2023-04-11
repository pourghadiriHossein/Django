from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=14, unique=True, null=True, blank=True)
    status = models.SmallIntegerField(default=1)