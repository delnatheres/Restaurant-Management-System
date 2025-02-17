# Generated by Django 5.1.4 on 2025-01-12 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0080_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('available', 'Available'), ('reserved', 'Reserved')], max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.table'),
        ),
    ]
