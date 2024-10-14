# Generated by Django 5.1 on 2024-10-14 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0059_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.signin')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.menuitem')),
            ],
            options={
                'unique_together': {('customer', 'menu_item')},
            },
        ),
    ]