# Generated by Django 4.0.4 on 2022-06-06 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_userid_listing_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment',
            field=models.CharField(default='nothing', max_length=200),
        ),
        migrations.AddField(
            model_name='comments',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='list',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='comment_list', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
