# Generated by Django 4.2.7 on 2023-12-13 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_occurrence_timeofday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='timeofday',
            field=models.DateTimeField(null=True),
        ),
    ]
