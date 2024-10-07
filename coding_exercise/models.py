from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from student.models import Student

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=50)
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    test_cases = models.TextField(help_text="Define test cases as Python/Java/C code")

    def __str__(self):
        return self.title

