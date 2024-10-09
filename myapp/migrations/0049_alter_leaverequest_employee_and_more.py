# Generated by Django 5.1 on 2024-10-08 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0048_alter_feedback_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='myapp.employee'),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='leave_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]