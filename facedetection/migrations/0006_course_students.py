# Generated by Django 4.1.7 on 2023-11-04 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facedetection', '0005_alter_students_face_embedding'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, to='facedetection.students'),
        ),
    ]
