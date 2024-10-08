from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Course, UserCourseProgress  # Import the models
from user.models import User

# Course Resource
class CourseResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by__username',  # Assuming username is the desired attribute to import/export
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')  # Use the username to link to the User model
    )

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_description', 'created_by', 'created_at', 'updated_at')

# UserCourseProgress Resource
class UserCourseProgressResource(resources.ModelResource):
    user = fields.Field(
        column_name='user__username',  # Assuming username is the desired attribute to import/export
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')  # Use the username to link to the User model
    )
    course = fields.Field(
        column_name='course__course_name',  # Assuming course_name is the desired attribute to import/export
        attribute='course',
        widget=ForeignKeyWidget(Course, 'course_name')  # Use course_name to link to the Course model
    )

    class Meta:
        model = UserCourseProgress
        fields = ('id', 'user', 'course', 'progress_percentage', 'last_accessed')

# Admin registration for Course
@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ('course_name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('course_name', 'created_by__username')  # Searchable fields
    list_filter = ('created_by',)  # Filter by created_by

# Admin registration for UserCourseProgress
@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(ImportExportModelAdmin):
    resource_class = UserCourseProgressResource
    list_display = ('user', 'course', 'progress_percentage', 'last_accessed')
    search_fields = ('user__username', 'course__course_name')  # Searchable fields
    list_filter = ('user', 'course')  # Filter by user and course
