# Generated by Django 4.2.5 on 2023-10-20 20:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', through='network.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]
