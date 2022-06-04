# Generated by Django 4.0.4 on 2022-06-04 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_value',
            field=models.FloatField(default='0'),
        ),
        migrations.AddField(
            model_name='bid',
            name='list',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='list', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='use', to=settings.AUTH_USER_MODEL),
        ),
    ]
