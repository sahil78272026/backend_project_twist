from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models



class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",    # Avoids conflict with default 'user_set'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Avoids conflict with default 'user_set'
        blank=True
    )

    def __str__(self):
        return self.username
