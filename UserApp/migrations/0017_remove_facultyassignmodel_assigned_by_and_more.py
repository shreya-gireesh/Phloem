# Generated by Django 5.1 on 2024-09-04 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0016_studentfilemodel_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultyassignmodel',
            name='assigned_by',
        ),
        migrations.RemoveField(
            model_name='facultyassignmodel',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='facultyassignmodel',
            name='file',
        ),
        migrations.DeleteModel(
            name='ManagerModel',
        ),
        migrations.DeleteModel(
            name='TeachersModel',
        ),
        migrations.DeleteModel(
            name='FacultyAssignModel',
        ),
    ]
