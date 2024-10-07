
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Submission

# Create a resource class for the Submission model
class SubmissionResource(resources.ModelResource):
    class Meta:
        model = Submission
        # Optionally, specify fields to include or exclude
        # fields = ('student', 'exercise', 'code', 'created_at', 'score')
        # exclude = ('id',)

# Register the Submission model with import/export functionality
@admin.register(Submission)
class SubmissionAdmin(ImportExportModelAdmin):
    resource_class = SubmissionResource
    list_display = ('student', 'exercise', 'created_at', 'score')  # Customize the list display



# # Register your models here.
# @admin.register(Exercise)
# class ExerciseAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'language')
#     search_fields = ('title',)

# @admin.register(Submission)
# class SubmissionAdmin(admin.ModelAdmin):
#     list_display = ('exercise', 'student', 'created_at', 'score')
#     search_fields = ('exercise__title', 'submission__student')
#     list_filter = ('exercise',)
#     readonly_fields = ('created_at',)

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         return queryset.select_related('exercise', 'student')