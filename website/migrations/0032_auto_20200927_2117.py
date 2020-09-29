# Generated by Django 3.1.1 on 2020-09-27 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_auto_20200927_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
