from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Subject, Category, Material

# Define Resource classes for import/export functionality
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'code')  # Define fields to be imported/exported


class CategoryResource(resources.ModelResource):
    subject = fields.Field(
        column_name='subject__name',  # This should match the column name in your import file
        attribute='subject',
        widget=ForeignKeyWidget(Subject, 'name')  # Use the 'name' field to match the subject
    )

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'subject')  # Include 'subject' directly as it is a ForeignKey

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
