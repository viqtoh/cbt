# Generated by Django 4.2.4 on 2023-09-08 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0016_course_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdetails',
            name='reg',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='course',
            name='last_active',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
