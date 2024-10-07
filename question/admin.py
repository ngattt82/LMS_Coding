# admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Question, Answer

# Resource class for Question
class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ('id', 'subject', 'category', 'correct_answer', 'question_text', 'created_at')  # Customize fields for export

# Resource class for Answer
class AnswerResource(resources.ModelResource):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'text', 'is_correct')  # Customize fields for export

# Register Question with import/export functionality
@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('question_text', 'correct_answer', 'created_at')  # Customize the list display

# Register Answer with import/export functionality
@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    resource_class = AnswerResource
    list_display = ('text', 'is_correct', 'question')  # Customize the list display
