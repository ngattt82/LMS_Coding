# Generated by Django 5.0.9 on 2024-10-09 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_group', '0001_initial'),
        ('training_program', '0001_initial'),
        ('user', '0002_user_training_programs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='modules',
            field=models.ManyToManyField(blank=True, related_name='assigned_users', to='module_group.module'),
        ),
        migrations.AlterField(
            model_name='user',
            name='training_programs',
            field=models.ManyToManyField(to='training_program.trainingprogram'),
        ),
    ]
