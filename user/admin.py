# admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User  # Adjust the import path as necessary

# Resource class for User
class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')  # Specify fields to include in import/export

# Register User with import/export functionality
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
