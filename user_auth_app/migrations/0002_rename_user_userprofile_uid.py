# Generated by Django 5.1.2 on 2024-11-01 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='uid',
        ),
    ]
