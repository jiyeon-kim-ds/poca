from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.IntegerField(default=10000, help_text="cash")
