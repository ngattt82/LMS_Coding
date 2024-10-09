from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import User
from training_program.models import TrainingProgram
from module_group.models import Module

# Define Resource class for User model
class UserResource(resources.ModelResource):
    training_programs = fields.Field(
        column_name='training_programs__name',
        attribute='training_programs',
        widget=ForeignKeyWidget(TrainingProgram, 'name')
    )
    modules = fields.Field(
        column_name='modules',
        attribute='modules',
        widget=ManyToManyWidget(Module, 'module_name')
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'training_programs', 'modules')

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    resource_class = UserResource
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'training_programs', 'modules', 'password'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Make the date_joined field read-only
        return ['date_joined']

    def save_model(self, request, obj, form, change):
        # Ensure password is hashed before saving
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])  # Hash the password
        super().save_model(request, obj, form, change)
