# Generated by Django 4.0.4 on 2022-06-06 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_comments_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='listwatchlist',
            new_name='list',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='userwatchlist',
            new_name='user',
        ),
    ]