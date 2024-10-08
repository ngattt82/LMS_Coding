from django.db import models
import mimetypes
import os

from django.db import models
from django.core.exceptions import ValidationError

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)  # New code field

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject, related_name='categories', blank=True)

    class Meta:
        unique_together = ('category_name',)

    def __str__(self):
        return self.category_name

    def get_descendants(self):
        descendants = set()
        subs = self.subcategories.all()
        for sub in subs:
            descendants.add(sub)
            descendants.update(sub.get_descendants())
        return descendants

    def save(self, *args, **kwargs):
        self.category_name = self.category_name.lower()
        super().save(*args, **kwargs)
        self.update_subcategories_subjects()

    def update_subcategories_subjects(self):
        for subcategory in self.subcategories.all():
            subcategory.subjects.set(self.subjects.all())
            subcategory.save()

class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subcategory_name', 'parent_category')

    def __str__(self):
        return self.subcategory_name

    def clean(self):
        # Check if a category with the same name exists (case-sensitive)
        if Category.objects.filter(category_name__exact=self.subcategory_name).exists():
            raise ValidationError("A category with this exact name already exists.")

    def save(self, *args, **kwargs):
        self.subcategory_name = self.subcategory_name.lower()
        self.clean()
        super().save(*args, **kwargs)
        # Inherit subjects from parent category
        self.subjects.set(self.parent_category.subjects.all())

    @property
    def subjects(self):
        return self.parent_category.subjects
       
class Material(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('assignments', 'Assignments'),
        ('labs', 'Labs'),
        ('lectures', 'Lectures'),
        ('references', 'References'),  # New material type
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='')  # We will customize the upload path in a method
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.get_material_type_display()}"

    def get_file_type(self):
        """Returns the MIME type of the file."""
        if self.file:
            mime_type, _ = mimetypes.guess_type(self.file.name)
            return mime_type or 'Unknown'
        return 'No file'

    def save(self, *args, **kwargs):
        # Generate the folder path dynamically based on subject's code and material type
        self.file.field.upload_to = self.get_upload_path()
        super().save(*args, **kwargs)

    def get_upload_path(self):
        """Returns the upload path based on the subject code and material type."""
        return os.path.join(self.subject.code, self.material_type)


