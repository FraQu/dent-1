# Generated by Django 3.1.1 on 2020-09-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_remove_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
