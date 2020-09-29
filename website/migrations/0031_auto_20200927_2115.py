# Generated by Django 3.1.1 on 2020-09-27 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_auto_20200927_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.AddField(
            model_name='customer',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.user'),
            preserve_default=False,
        ),
    ]
