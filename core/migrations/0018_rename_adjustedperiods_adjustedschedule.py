# Generated by Django 4.2.7 on 2024-02-13 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_defaultroutine_date_adjustedperiods'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdjustedPeriods',
            new_name='AdjustedSchedule',
        ),
    ]
