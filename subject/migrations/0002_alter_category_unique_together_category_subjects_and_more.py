# Generated by Django 5.0.9 on 2024-10-08 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('category_name',)},
        ),
        migrations.AddField(
            model_name='category',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='categories', to='subject.subject'),
        ),
        migrations.RemoveField(
            model_name='category',
            name='subject',
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=255)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='subject.category')),
            ],
            options={
                'unique_together': {('subcategory_name', 'parent_category')},
            },
        ),
    ]
