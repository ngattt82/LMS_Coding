# admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Quiz, Submission, SubmittedAnswer

# Resource class for Quiz
class QuizResource(resources.ModelResource):
    class Meta:
        model = Quiz
        fields = ('id', 'subject', 'category', 'title', 'created_at', 'created_by', 'due_date', 'attempts_allowed', 'grading_method')

# Resource class for Submission
class SubmissionResource(resources.ModelResource):
    class Meta:
        model = Submission
        fields = ('id', 'quiz', 'student', 'submitted_at', 'grade', 'submitted_file')

# Resource class for SubmittedAnswer
class SubmittedAnswerResource(resources.ModelResource):
    class Meta:
        model = SubmittedAnswer
        fields = ('id', 'submission', 'question', 'text')

# Register Quiz with import/export functionality
@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    resource_class = QuizResource
    list_display = ('title', 'subject', 'category', 'created_at', 'created_by', 'due_date', 'attempts_allowed')

# Register Submission with import/export functionality
@admin.register(Submission)
class SubmissionAdmin(ImportExportModelAdmin):
    resource_class = SubmissionResource
    list_display = ('quiz', 'student', 'submitted_at', 'grade')

# Register SubmittedAnswer with import/export functionality
@admin.register(SubmittedAnswer)
class SubmittedAnswerAdmin(ImportExportModelAdmin):
    resource_class = SubmittedAnswerResource
    list_display = ('submission', 'question', 'text')
