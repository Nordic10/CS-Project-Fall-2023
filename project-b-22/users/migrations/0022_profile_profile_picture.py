# Generated by Django 4.2.6 on 2023-11-13 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/admin/images/defaultPFP.png', null=True, upload_to='profile_pictures/'),
        ),
    ]
