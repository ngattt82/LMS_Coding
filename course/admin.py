from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Course, Session, CourseMaterial, Document, Video, Enrollment, ReadingMaterial, Completion, SessionCompletion

# Define resources for import/export
class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

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
