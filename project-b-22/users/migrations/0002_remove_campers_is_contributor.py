# Generated by Django 4.2.5 on 2023-10-07 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campers',
            name='is_contributor',
        ),
    ]
