# Generated by Django 4.2.7 on 2024-02-12 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_period_period_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='period',
            name='subjects',
        ),
        migrations.AddField(
            model_name='period',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.subject'),
        ),
    ]
