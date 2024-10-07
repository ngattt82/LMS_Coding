from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Additional fields can be added here
    date_joined = models.DateTimeField(auto_now_add=True)

    # Override the groups field to prevent conflicts with the default User model
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_name='custom_user_groups',  # Added related_name
    )

    # Override the user_permissions field to prevent conflicts with the default User model
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_name='custom_user_permissions',  # Added related_name
    )
