# Generated by Django 5.1 on 2024-09-29 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_menuitem_feedback_order_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]