# Generated by Django 5.0.9 on 2024-10-09 00:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('test_cases', models.TextField(help_text='Define test cases as Python/Java/C code')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding_exercise.programminglanguage')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding_exercise.exercise')),
            ],
        ),
    ]
