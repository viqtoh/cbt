# Generated by Django 4.2.4 on 2023-09-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0009_alter_examination_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='status',
            field=models.CharField(default='running', max_length=7),
        ),
    ]
