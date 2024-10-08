# Generated by Django 5.1 on 2024-09-04 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0008_delete_studentmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfilemodel',
            name='company_specific',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentfilemodel',
            name='company_specific_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentfilemodel',
            name='country_specific',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentfilemodel',
            name='country_specific_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
