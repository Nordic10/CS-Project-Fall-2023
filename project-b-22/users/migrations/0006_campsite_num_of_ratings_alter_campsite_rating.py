# Generated by Django 4.2.5 on 2023-10-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_campsite_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='campsite',
            name='num_of_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='campsite',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2),
        ),
    ]
