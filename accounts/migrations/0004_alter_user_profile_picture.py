# Generated by Django 4.1.7 on 2023-03-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default_avatar.png', upload_to='profile_pictures/uploaded_by_users/'),
        ),
    ]