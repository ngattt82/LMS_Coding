from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Category, Material


# Define Resource classes for import/export functionality
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'code')  # Define fields to be imported/exported

from import_export.fields import Field

class CategoryResource(resources.ModelResource):
    subject_name = Field(attribute='subject__name', column_name='subject__name')

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'subject_name')  # Include subject_name in fields


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('category_name', 'subject')  # Ensure subject is displayed
    search_fields = ('category_name', 'subject__name')


    
class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        fields = ('id', 'subject__name', 'material_type', 'file', 'google_drive_link', 'uploaded_at')


# Define Admin classes with ImportExportModelAdmin
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code')

@admin.register(Material)
class MaterialAdmin(ImportExportModelAdmin):
    resource_class = MaterialResource
    list_display = ('subject', 'material_type', 'google_drive_link', 'uploaded_at')
    search_fields = ('subject__name', 'material_type')
    list_filter = ('material_type', 'subject')
