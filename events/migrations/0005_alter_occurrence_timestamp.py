# Generated by Django 4.2.7 on 2023-11-20 05:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_rename_occurence_occurrence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
