from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

# User model
class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_name='custom_user_groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_name='custom_user_permissions',
    )


