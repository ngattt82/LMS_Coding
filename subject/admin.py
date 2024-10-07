# admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Material

# Resource class for Subject
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'code')

# Register Subject with import/export functionality
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_display = ('name', 'description', 'code')

# Resource class for Material
class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        fields = ('id', 'subject', 'material_type', 'file', 'uploaded_at')

# Register Material with import/export functionality
@admin.register(Material)
class MaterialAdmin(ImportExportModelAdmin):
    resource_class = MaterialResource
    list_display = ('subject', 'material_type', 'file', 'uploaded_at')
