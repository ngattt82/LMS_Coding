from django.db import models
# from user.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    creator = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_courses')
    instructor = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_courses')
    published = models.BooleanField(default=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='is_prerequisite_for')

    def __str__(self):
        return self.name

    def get_completion_percent(self, user):
        total_sessions = self.sessions.count()
        completed_sessions = SessionCompletion.objects.filter(session__course=self, user=user, completed=True).count()
        return (completed_sessions / total_sessions) * 100 if total_sessions > 0 else 0


class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions', null=True)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()  # Order of appearance

    def __str__(self):
        return self.name


class CourseMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('document', 'Document'),
        ('video', 'Video'),
        ('reading', 'Reading Material'),
    ]
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='materials', null=True)
    material_id = models.PositiveIntegerField()  # Make sure this uniquely identifies the material
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES)
    order = models.PositiveIntegerField()  # Order of appearance
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'session id: {self.session.id}   title: {self.title}'

    class Meta:
        ordering = ['order']


class Document(models.Model):
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='documents', null=True)
    doc_title = models.CharField(max_length=255)
    doc_file = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.doc_title


class Video(models.Model):
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='videos', null=True)
    vid_title = models.CharField(max_length=255)
    vid_file = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.vid_title


class Enrollment(models.Model):
    student = models.ForeignKey('user.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"


class ReadingMaterial(models.Model):
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='reading_materials', null=True)
    content = RichTextUploadingField()  # Use RichTextUploadingField for HTML content with file upload capability
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Completion(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('session', 'material', 'user')

    def __str__(self):
        return f"Completion for {self.material} in {self.session}"


class SessionCompletion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('course', 'user', 'session')  # Ensures a user can only complete a session once

    def __str__(self):
        return f"{self.user} completed session: {self.session.name}"


def mark_session_complete(course, user, session):
    # Count the total materials in the session
    total_materials = session.materials.count()

    # Count completed materials by checking the Completion model
    completed_materials = Completion.objects.filter(session=session, user=user, completed=True).count()

    # Check if all materials are completed
    if total_materials == completed_materials:
        # Mark the session as complete in the SessionCompletion model
        SessionCompletion.objects.update_or_create(
            user=user,
            session=session,
            defaults={'completed': True}
        )
