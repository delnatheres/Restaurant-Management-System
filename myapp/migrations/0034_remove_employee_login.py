# Generated by Django 5.1 on 2024-10-02 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_leaverequest_employeedashboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='login',
        ),
    ]