# Generated by Django 4.2.5 on 2023-11-05 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='campsite',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='campsite',
            name='long',
            field=models.FloatField(default=0),
        ),
    ]
