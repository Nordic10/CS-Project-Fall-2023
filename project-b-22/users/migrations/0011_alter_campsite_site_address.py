# Generated by Django 4.2.5 on 2023-10-31 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_campsite_site_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campsite',
            name='site_address',
            field=models.CharField(default='placeholder Dr.', max_length=100),
        ),
    ]
