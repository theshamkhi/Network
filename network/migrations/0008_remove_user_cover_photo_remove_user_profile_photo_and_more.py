# Generated by Django 4.2.5 on 2023-10-22 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_user_cover_photo_user_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cover_photo',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_photo',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
