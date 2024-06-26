# Generated by Django 5.0.3 on 2024-03-21 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='menu_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='purchase',
            name='item_price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='item_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.menuitem'),
        ),
    ]
