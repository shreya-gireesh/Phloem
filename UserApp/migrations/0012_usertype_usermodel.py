# Generated by Django 5.1 on 2024-09-04 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0011_managermodel_facultyassignmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('usertype_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_type', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Manager', 'Manager')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('mailid', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.usertype')),
            ],
        ),
    ]
