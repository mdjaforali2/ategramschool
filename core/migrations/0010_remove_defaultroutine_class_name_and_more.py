# Generated by Django 4.2.7 on 2024-02-12 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_period_end_time_period_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defaultroutine',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='defaultroutine',
            name='subject',
        ),
    ]