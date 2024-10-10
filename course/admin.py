from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin

from import_export.widgets import ForeignKeyWidget
from user.models import User
# Define resources for import/export
class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

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

# Admin registration for UserCourseProgress
@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(ImportExportModelAdmin):
    resource_class = UserCourseProgressResource
    list_display = ('user', 'course', 'progress_percentage', 'last_accessed')
    search_fields = ('user__username', 'course__course_name')  # Searchable fields
    list_filter = ('user', 'course')  # Filter by user and course
class SessionResource(resources.ModelResource):
    class Meta:
        model = Session

class CourseMaterialResource(resources.ModelResource):
    class Meta:
        model = CourseMaterial

class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

class EnrollmentResource(resources.ModelResource):
    class Meta:
        model = Enrollment

class ReadingMaterialResource(resources.ModelResource):
    class Meta:
        model = ReadingMaterial

class CompletionResource(resources.ModelResource):
    class Meta:
        model = Completion

class SessionCompletionResource(resources.ModelResource):
    class Meta:
        model = SessionCompletion


# Register models in Django Admin with import/export functionality
@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource

@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    resource_class = SessionResource

@admin.register(CourseMaterial)
class CourseMaterialAdmin(ImportExportModelAdmin):
    resource_class = CourseMaterialResource

@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    resource_class = DocumentResource

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource

@admin.register(Enrollment)
class EnrollmentAdmin(ImportExportModelAdmin):
    resource_class = EnrollmentResource

@admin.register(ReadingMaterial)
class ReadingMaterialAdmin(ImportExportModelAdmin):
    resource_class = ReadingMaterialResource

@admin.register(Completion)
class CompletionAdmin(ImportExportModelAdmin):
    resource_class = CompletionResource

@admin.register(SessionCompletion)
class SessionCompletionAdmin(ImportExportModelAdmin):
    resource_class = SessionCompletionResource
