# Generated by Django 5.1 on 2024-09-10 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0027_alter_facultyassignmodel_assigned_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuploadsmodel',
            name='countrycode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UserApp.countrycodemodel'),
        ),
    ]
