# Generated by Django 4.2.4 on 2023-09-04 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_course_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='recent',
            new_name='active',
        ),
    ]
