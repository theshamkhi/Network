# Generated by Django 4.2.5 on 2023-10-25 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(upload_to='profile_pics/'),
        ),
    ]
