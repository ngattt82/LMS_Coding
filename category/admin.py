from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('category_name', 'subject')  # Customize as needed
