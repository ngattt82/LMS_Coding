# admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ProgrammingLanguage, Exercise

# Define resources for the models
class ProgrammingLanguageResource(resources.ModelResource):
    class Meta:
        model = ProgrammingLanguage

class ExerciseResource(resources.ModelResource):
    class Meta:
        model = Exercise

# Register your models with the admin
@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(ImportExportModelAdmin):
    resource_class = ProgrammingLanguageResource
    list_display = ('name',)  # Customize as needed

@admin.register(Exercise)
class ExerciseAdmin(ImportExportModelAdmin):
    resource_class = ExerciseResource
    list_display = ('title', 'language')  # Customize as needed
