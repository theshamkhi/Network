# Generated by Django 4.2.5 on 2023-10-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', upload_to='profile_pics/'),
        ),
    ]
