# Generated by Django 4.2.7 on 2024-02-11 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_schedule_room_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='class_name',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
