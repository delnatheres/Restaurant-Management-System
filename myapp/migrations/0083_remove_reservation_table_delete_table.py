# Generated by Django 5.1.4 on 2025-01-12 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0082_remove_table_status_table_is_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='table',
        ),
        migrations.DeleteModel(
            name='Table',
        ),
    ]
