# Generated by Django 3.1.1 on 2020-09-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20200913_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='updated_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]