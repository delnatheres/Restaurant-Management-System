# Generated by Django 5.1 on 2024-09-24 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_login_reset_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=10)),
                ('joinedon', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
