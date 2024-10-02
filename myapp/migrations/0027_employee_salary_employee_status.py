# Generated by Django 5.1 on 2024-10-01 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_remove_staffprofile_user_delete_leave_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]