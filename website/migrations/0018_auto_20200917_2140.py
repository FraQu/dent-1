# Generated by Django 3.1.1 on 2020-09-17 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_auto_20200917_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_doctor',
        ),
        migrations.AddField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]