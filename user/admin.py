from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .widgets import PasswordWidget 

class UserResource(resources.ModelResource):
    password = fields.Field(
        column_name='password',
        attribute='password',
        widget=PasswordWidget()  
    )
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        exclude = ('password',)  
        export_order = ('id', 'username', 'email', 'first_name', 'last_name')
    
    def dehydrate_password(self, user):
        return ""  

class CustomUserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    resource_class = UserResource
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    readonly_fields = ('date_joined',)  

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)

