from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from coding_exercise.models import Exercise
from django.conf import settings

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.exercise.title}"
