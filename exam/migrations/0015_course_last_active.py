# Generated by Django 4.2.4 on 2023-09-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0014_studentdetails_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='last_active',
            field=models.DateTimeField(null=True),
        ),
    ]
