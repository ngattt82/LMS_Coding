from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from training_program.models import TrainingProgram
from module_group.models import Module

# User model
class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)

# Custom user model
class CustomUser(models.Model):  # Inherit from models.Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    training_programs = models.ManyToManyField(TrainingProgram, related_name='users')  # Specify 'TrainingProgram' if it's in another app

    # Add many-to-many relationship for assigned modules
    modules = models.ManyToManyField(Module, related_name='assigned_users', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


    # groups = models.ManyToManyField(
    #     Group,
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups',
    #     related_name='custom_user_groups',
    # )

    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    #     related_name='custom_user_permissions',
    # )


