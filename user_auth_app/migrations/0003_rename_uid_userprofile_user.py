# Generated by Django 5.1.2 on 2024-11-01 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0002_rename_user_userprofile_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='uid',
            new_name='user',
        ),
    ]