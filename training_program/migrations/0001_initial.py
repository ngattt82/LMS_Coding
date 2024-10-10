# Generated by Django 5.1.1 on 2024-10-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '0001_initial'),
        ('subject_course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=255, unique=True)),
                ('program_code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('courses', models.ManyToManyField(blank=True, related_name='training_programs', to='subject_course.course')),
                ('subjects', models.ManyToManyField(blank=True, related_name='programs', to='subject.subject')),
            ],
        ),
    ]
