from django import forms
from .models import Exercise, Submission


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'description', 'language', 'test_cases']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'id': 'code-editor'}),  # Thêm id 'code-editor'
        }
