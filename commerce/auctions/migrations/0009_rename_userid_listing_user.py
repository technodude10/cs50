# Generated by Django 4.0.4 on 2022-06-06 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_bid_one_bid_listing_open_or_close'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='userid',
            new_name='user',
        ),
    ]
