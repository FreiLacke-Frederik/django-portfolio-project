# Generated by Django 5.0.3 on 2024-04-09 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_purchase_purchase_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='item_price',
            new_name='price',
        ),
    ]
