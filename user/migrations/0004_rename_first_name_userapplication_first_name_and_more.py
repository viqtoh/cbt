# Generated by Django 4.2.4 on 2023-08-16 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_userapplication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userapplication',
            old_name='first_name',
            new_name='First_name',
        ),
        migrations.RenameField(
            model_name='userapplication',
            old_name='last_name',
            new_name='Last_name',
        ),
        migrations.RemoveField(
            model_name='userapplication',
            name='Date_of_birth',
        ),
    ]
