# Generated by Django 4.2.7 on 2023-11-30 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test', '0010_alter_slotcatalog_iframe_game_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slotcatalog',
            name='slug',
            field=models.SlugField(default=None, max_length=255, unique=True),
        ),
    ]
