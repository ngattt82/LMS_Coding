from django.db import models
from subject.models import Subject
from course.models import Course
class TrainingProgram(models.Model):
    program_name = models.CharField(max_length=255, unique=True)
    program_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Cho phép subjects có thể để trống
    subjects = models.ManyToManyField(Subject, related_name='programs', blank=True)
    courses = models.ManyToManyField(Course, related_name='training_programs', blank=True)     


    def __str__(self):
        return self.program_name
