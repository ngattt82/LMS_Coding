from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Course  # Import the Course model
# Register your models here.
# Define resource classes for import/export functionality
class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_description', 'subject__name')  # Add related subject's name
# Registering models in admin with import/export functionality

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ('course_name', 'subject')
    search_fields = ('course_name', 'subject__name')
    list_filter = ('subject',)