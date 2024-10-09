from django.db import models
from subject.models import Subject

class TrainingProgram(models.Model):
    program_name = models.CharField(max_length=255, unique=True)
    program_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    subjects = models.ManyToManyField(Subject, related_name='programs')  # Many-to-many relationship

    def __str__(self):
        return self.program_name

