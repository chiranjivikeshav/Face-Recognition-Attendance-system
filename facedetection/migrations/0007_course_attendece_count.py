# Generated by Django 4.1.7 on 2023-11-09 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facedetection', '0006_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='attendece_count',
            field=models.IntegerField(default=0),
        ),
    ]
