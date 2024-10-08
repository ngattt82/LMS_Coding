from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import ProgrammingLanguage, Exercise, Submission
from import_export.widgets import ForeignKeyWidget
# Define resource for each model

class ProgrammingLanguageResource(resources.ModelResource):
    class Meta:
        model = ProgrammingLanguage
        fields = ('id', 'name')  # Specify fields to be exported/imported

# resources.py

class ExerciseResource(resources.ModelResource):
    language = fields.Field(
        column_name='language',
        attribute='language',
        widget=ForeignKeyWidget(ProgrammingLanguage, 'name')  # Use 'id' if you have IDs in the Excel file
    )

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'language', 'test_cases')  # Ensure 'language' is included


class SubmissionResource(resources.ModelResource):
    class Meta:
        model = Submission
        fields = ('id', 'student__username', 'exercise__title', 'code', 'created_at', 'score')  # Include ForeignKeys


# Register models with ImportExportModelAdmin

@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(ImportExportModelAdmin):
    resource_class = ProgrammingLanguageResource

@admin.register(Exercise)
class ExerciseAdmin(ImportExportModelAdmin):
    resource_class = ExerciseResource

# admin.py
@admin.register(Submission)
class SubmissionAdmin(ImportExportModelAdmin):
    resource_class = SubmissionResource
    list_display = ('student', 'exercise', 'created_at', 'score')  # Customize this as needed
