# Generated by Django 3.1.1 on 2020-10-20 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20201020_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='employee',
        ),
        migrations.AddField(
            model_name='customer',
            name='employee',
            field=models.ManyToManyField(null=True, to='website.Employee'),
        ),
    ]
