# Generated by Django 5.0.3 on 2024-04-08 10:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_ingredient_price_per_kilo'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='purchase_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
