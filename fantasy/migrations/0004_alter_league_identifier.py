# Generated by Django 5.0.2 on 2024-02-21 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0003_league_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='identifier',
            field=models.CharField(blank=True, editable=False, max_length=12, unique=True),
        ),
    ]
