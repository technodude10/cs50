# Generated by Django 4.0.4 on 2022-06-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_bid_value_bid_list_bid_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.FloatField(default='0'),
        ),
    ]
