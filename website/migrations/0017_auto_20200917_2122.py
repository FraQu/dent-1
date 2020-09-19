# Generated by Django 3.1.1 on 2020-09-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_auto_20200913_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='email',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
    ]